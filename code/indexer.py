import re
import sys
import jieba


def build(input_content_file, output_doc_length_file, output_doc_freq_file, output_index_file=None, isIndex=False):
    index = {}
    df = {}
    doc_len = {}

    with open(input_content_file, 'r') as file:
        line_cnt = 0
        for line in file:
            doc_index = {}
            line_cnt += 1
            if line_cnt % 5000 == 0:
                print '\tBUILD DOCF', line_cnt
            attr = re.split('[\t ]+', line.strip())
            if len(attr) < 2:
                continue
            uid = attr[0].strip() # .encode('utf-8', 'ignore')
            words = attr[1:]
            doc_len[uid] = len(words)
            # words = jieba.cut(content) # word segmentation
            for w in words:
                w = w.strip().decode('utf-8', 'ignore').lower()
                if w not in doc_index:
                    doc_index[w] = 0
                doc_index[w] += 1

            for w, freq in doc_index.items():
                if isIndex:
                    if w not in index:
                        index[w] = {}
                    index[w][uid] = freq
                if w not in df:
                    df[w] = 0
                df[w] += 1
    print '\tRead docs done!'

    with open(output_doc_length_file, 'w') as file:
        for doc, length in doc_len.items():
            file.write('%s\t%d\n'%(doc, length))
    print '\tDoc len done!'

    with open(output_doc_freq_file, 'w') as file:
        for w, f in df.items():
            w = w.encode('utf-8', 'ignore')
            file.write('%s\t%d\n' % (w, f))
    print '\tDf done!'

    if isIndex:
        with open(output_index_file, 'w') as file:
            for w, u_f in index.items():
                u_f_list = ['%s,%d' % (u, f) for u, f in u_f.items()]
                file.write(w.encode('utf-8', 'ignore') + '\t' + ':'.join(u_f_list) + '\n')
        print '\tIndex done!'


def make_queries(input_content_file, input_qrel_file, input_qid_file, output_queries_file):
    uids = {}
    with open(input_content_file) as file:
        cnt = 0
        for line in file:
            cnt += 1
            if cnt % 5000 == 0:
                print '\tREAD UIDS', cnt
            attr = re.split('[\t ]+', line.strip())
            uid = attr[0]
            uids[uid] = 0
    # uids = list(set(uids))
    print '\tuids length:', len(uids)

    qid_uids_dict = {}
    qid_rels_dict = {}

    with open(input_qrel_file) as file:
        cnt = 0
        for line in file:
            cnt += 1
            if cnt % 5000 == 0:
                print '\tREAD QRELS', cnt
            attr = re.split('[\t ]+', line.strip())
            qid = attr[0].strip()
            uid = attr[1].strip()
            # rel = ':'.join(attr[2:]).strip()
            if uid not in uids:
                continue
            if qid not in qid_uids_dict:
                qid_uids_dict[qid] = []

            # if qid not in qid_rels_dict:
            #     qid_rels_dict[qid] = []

            qid_uids_dict[qid].append(uid)
            # qid_rels_dict[qid].append(rel)

            # if qid not in qid_uids_rel_dict:
            #     qid_uids_rel_dict[qid] = {}
            # if uid not in qid_uids_rel_dict[qid]:
            #     qid_uids_rel_dict[qid][uid] = rel

    print '\tqid_uids_dict', len(qid_uids_dict)

    qid_query_dict = {}

    with open(input_qid_file) as file:
        for line in file:
            attr = re.split('[\t ]+', line.strip())
            qid = attr[0].strip()
            query = attr[1:]
            qid_query_dict[qid] = ' '.join(query).lower()

    with open(output_queries_file, 'w') as output:
        for qid in qid_uids_dict:
            if qid not in qid_query_dict:
                continue
            output.write(qid+'\t'+qid_query_dict[qid] + '\t' + ' '.join(qid_uids_dict[qid])+'\n') #  +'\t'+' '.join(qid_rels_dict[qid])+ '\n')
            # output.write(qid + '\t' + qid_query_dict[qid] + '\t' + ' '.join(qid_uids_dict[qid]) +'\t'+' '.join(qid_rels_dict[qid])+ '\n')

#
# if __name__ == "__main__":
#     root_dir = '../'
#
#     # 50_test_title input
#     _qid_file = root_dir + 'data/50_test_title/50_test_qid_seg.txt'  # qid\tquery
#     _qrel_file = root_dir + 'data/50_test_title/50_test_qrels.txt'  # qid docid
#     _content_file = root_dir + 'data/50_test_title/50_test_title_seg.txt'  # docid\tcontent
#     suffix = '_50_test_title'
#     #
#     # # # ntcir small input
#     # # _qid_file = 'data/ntcir_small/test_ntcir_qid_seg.txt' # qid\tquery
#     # # _qrel_file = 'data/ntcir_small/test_ntcir_small.qrels.txt' # qid docid
#     # # _content_file = 'data/ntcir_small/test_ntcir_title_seg_99112.txt' # docid\tcontent
#     # # suffix = '_ntcir_small'
#     #
#     # output
#     _doc_freq_file = root_dir + 'data/doc_freq/doc_freq' + suffix + '.txt'
#     _doc_length_file = root_dir + 'data/doc_length/doc_length' + suffix + '.txt'
#     _index_file = root_dir + 'data/index/index' + suffix + '.txt'
#     _queries_file = root_dir + 'data/queries/queries' + suffix + '.txt'
#
#     build(_content_file, _doc_length_file, _doc_freq_file, _index_file)
#     make_queries(_content_file, _qrel_file, _qid_file, _queries_file)
#     print 'done!'
