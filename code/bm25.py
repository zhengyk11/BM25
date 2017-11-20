import re
import math


class BM25():
    def __init__(self, config):
        self.doc_freq_file   = config['doc_freq_file_merge']
        self.doc_length_file = config['doc_length_file_merge']
        self.index_file      = config['index_file']
        self.queries_file    = config['queries_file']
        self.result_file     = config['result_file']

        # parameters for computation of bm25
        self.k1 = 1.2
        self.k2 = 100
        self.b = 0.75
        self.ri = 0.0
        self.R = 0.0

        self.avg_doc_len, self.doc_len_dict = self.cal_doc_len()
        self.num_of_docs = len(self.doc_len_dict)
        self.df = self.read_df()
        self.index = self.read_index()
        self.results = self.bm25_run()
        self.output_result()



    # calculate the doc length of each doc
    def cal_doc_len(self):
        doc_len_dict = {}
        total_doc_len = 0
        num_of_docs = 0

        with open(self.doc_length_file) as file:
            for line in file:
                num_of_docs += 1
                attr = re.split('[\t ]+', line.strip())
                if len(attr) != 2:
                    print 'cal_doc_len error at line %d' % num_of_docs
                    exit(0)
                docid = attr[0].strip()
                doc_length = int(attr[1])
                doc_len_dict[docid] = doc_length
                total_doc_len += doc_length

        avg_doc_len = float(total_doc_len) / num_of_docs
        return avg_doc_len, doc_len_dict


    # retrieving word and its frequency from the index
    def read_df(self):
        df = {}
        with open(self.doc_freq_file) as file:
            for line in file:
                attr = re.split('[\t ]+', line.strip())
                if len(attr) != 2:
                    continue
                w = attr[0].strip().lower()
                freq = int(attr[1])
                df[w] = freq
        return df


    def read_index(self):
        index = {}
        with open(self.index_file) as file:
            cnt = 0
            for line in file:
                cnt += 1
                if cnt % 5000 == 0:
                    print 'READ INDEX', cnt
                temp_dict = {}
                attr = re.split('[\t: ]+', line.strip())
                w = attr[0].strip().lower()
                if w not in index:
                    index[w] = {}
                # word = line.split()
                if len(attr) < 2:
                    continue
                u_f = attr[1:]
                # w = word[1].split(':')
                for item in u_f:
                    u, f = item.split(',')
                    u = u.strip()
                    f = int(f)
                    index[w][u] = f
        return index

    # compute the bm25 score
    def compute_bm_25(self, q, qf, bm_25_dict, uids):
        if q in self.index:
            for doc_id, df in self.index[q].items():
                if doc_id not in uids:
                    continue
                avdl = float((self.doc_len_dict[doc_id]) / self.avg_doc_len)
                k = self.k1 * ((1 - self.b) + self.b * avdl)
                idf = math.log((self.num_of_docs - self.df[q] + 0.5) / (self.df[q] + 0.5))
                score = idf * (((self.k1 + 1) * df) / (k + df)) * (((self.k2 + 1) * qf) / (self.k2 + qf))
                # score = (math.log(float(self.num_of_docs) / self.df[q])) \
                #         * (((self.k1 + 1) * df) / (k + df)) * (((self.k2 + 1) * qf) / (self.k2 + qf))
                # if doc_id in bm_25_dict: # .has_key() and bm_25_dict[doc_id] != -1000:
                bm_25_dict[doc_id] += score
                # else:
                #     bm_25_dict[doc_id] = score


    # read queries from query file
    def bm25_run(self):
        print 'bm25_run...'
        results = {}
        with open(self.queries_file) as file:
            for line in file:
                attr = line.strip().split('\t')
                qid = attr[0].strip()
                query = attr[1].lower()
                query_words = query.split()
                uids = attr[2].split()
                rels = map(float, attr[3].split())
                bm_25_dict = {}
                rel_dict = {}
                for uid, rel in zip(uids, rels):
                    if uid not in self.doc_len_dict:
                        continue
                    bm_25_dict[uid] = 0 # -1000
                    rel_dict[uid] = rel
                query_dict = {}

                for w in query_words:
                    if w in query_dict:
                        query_dict[w] += 1
                    else:
                        query_dict[w] = 1
                for k, v in query_dict.items():
                    self.compute_bm_25(k, v, bm_25_dict, uids)
                for uid in bm_25_dict:
                    if qid not in results:
                        results[qid] = {}
                    results[qid][uid] = [rel_dict[uid], bm_25_dict[uid]]
        return results


    def output_result(self):
        with open(self.result_file, 'w') as file:
            results = sorted(self.results.items(), key=lambda x:x[0])
            for qid, uid_score in results:
                for uid, rel_score in sorted(uid_score.items(), key=lambda x:x[1][1], reverse=True):
                    file.write('%s\t%s\t%f\t%f\n'%(qid, uid, rel_score[0], rel_score[1]))

