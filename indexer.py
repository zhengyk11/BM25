import sys
import jieba

# 50_test_title input
_qid_file = 'data/50_test_title/50_test_qid_seg.txt' # qid\tquery
_qrel_file = 'data/50_test_title/50_test_qrels.txt' # qid docid
_content_file = 'data/50_test_title/50_test_title_seg.txt' # docid\tcontent
suffix = '_50_test_title'

# # ntcir small input
# _qid_file = 'data/ntcir_small/test_ntcir_qid_seg.txt' # qid\tquery
# _qrel_file = 'data/ntcir_small/test_ntcir_small.qrels.txt' # qid docid
# _content_file = 'data/ntcir_small/test_ntcir_title_seg_99112.txt' # docid\tcontent
# suffix = '_ntcir_small'

#output
_key_freq_file = 'key_frep/key_freq' + suffix + '.txt'
_doc_length_file = 'doc_length/doc_length' + suffix + '.txt'
_index_file = 'index/index' + suffix + '.out'
_queries_file = 'queries/queries' + suffix + '.txt'

########################################
key_freq ={}
final_index = {}
doc_index_list = []


def build_index(doc_index_list):
    print len(doc_index_list)
    list_cnt = 0
    for i, val in enumerate(doc_index_list):
        list_cnt += 1
        if list_cnt % 5000 == 0:
            print list_cnt
        for k, v in val[1].items():
            temp = [val[0], str(v)]
            if k in final_index:
                final_index[k].append(temp)
            else:
                final_index[k] = [temp]

    print_final_dict(final_index)


def print_final_dict(final_index):
    fh = open(_index_file, 'w')
    for k in final_index:
        fh.write(k.encode('utf-8', 'ignore') + " ")
        fh.write(','.join(final_index[k][0]))
        for t in final_index[k][1:]:
            fh.write(':' + ','.join(t))
        fh.write("\n")


def build_docf():
    f_doc_length = open(_doc_length_file, 'w')
    input = open(_content_file, 'r')
    line_cnt = 0
    for line in input:
        line_cnt += 1
        if line_cnt % 500 == 0:
            print line_cnt
        try:
            doc_index = {}
            attr = line.strip().split('\t')
            uid = attr[0].strip()
            content = attr[1].strip()
            word = content.split(' ')
            # word = jieba.cut(content) # word segmentation
            word_set = []
            for w in word:
                w = w.decode('utf-8', 'ignore')
                word_set.append(w)
                if doc_index.has_key(w):
                    doc_index[w] += 1
                else:
                    doc_index[w] = 1
            if len(doc_index) > 0:
                doc_index_list.append([uid, doc_index])

            f_doc_length.write(str(uid) + " " + str(len(word_set)))
            f_doc_length.write("\n")
            word_set = list(set(word_set))
            for w in word_set:
                if key_freq.has_key(w):
                    key_freq[w] += 1
                else:
                    key_freq[w] = 1
        except:
            continue

    print 'read docs done! starting output key_freq...'
    fh = open(_key_freq_file, 'w')

    for k in key_freq.keys():
        fh.write(k.encode('utf-8', 'ignore') + " " + str(key_freq[k]))
        fh.write("\n")
    print 'output key_freq done! starting build_index...'
    build_index(doc_index_list)
    print 'build_index done!'
    fh.close()
    input.close()
    f_doc_length.close()

def make_queries():
    uids = set()
    file = open(_content_file, 'r')
    for line in file:
        uid = line.split('\t')[0]
        uids.add(uid)
    file.close()
    uids = list(uids)
    print 'uids length:', len(uids)

    qid_uids_dict = {}

    file = open(_qrel_file, 'r')

    for line in file:
        line = line.strip()
        attr = line.split(' ')
        qid = attr[0]
        uid = attr[1]
        if uid not in uids:
            continue
        if qid in qid_uids_dict:
            qid_uids_dict[qid].append(uid)
        else:
            qid_uids_dict[qid] = [uid]

    file.close()

    print len(qid_uids_dict)

    qid_query_dict = {}

    file = open(_qid_file, 'r')

    for line in file:
        line = line.strip()
        attr = line.split('\t')
        qid = attr[0]
        query = attr[1]
        # if qid in qid_uids_dict:
        qid_query_dict[qid] = query

    file.close()

    output = open(_queries_file, 'w')

    for qid in qid_uids_dict:
        output.write(qid + '\t' + qid_query_dict[qid] + '\t' + ' '.join(qid_uids_dict[qid]) + '\n')

    output.close()


if __name__ == "__main__":
    # newfile = _content_file
    build_docf()
    make_queries()
    print 'done!'