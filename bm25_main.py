import jieba
import sys, math

# suffix = '_ntcir_small'
suffix = '_50_test_title'

#input
_key_freq_file = 'key_frep/key_freq' + suffix + '.txt'
_doc_length_file = 'doc_length/doc_length' + suffix + '.txt'
_index_file = 'index/index' + suffix + '.out'
_queries_file = 'queries/queries' + suffix + '.txt'

#output
_result_file = 'results/results_2' + suffix + '.eval'


#################################
index ={}
doc_len_dict = {}
index_term_freq = {}
num_of_docs = 0
avg_doc_len = 0
total_doc_len = 0
final_index = {}

#calculate the doc length of each doc 
def cal_doc_len():
    global num_of_docs
    global total_doc_len
    global avg_doc_len
    f = open(_doc_length_file,'r')
    for line in f:
        num_of_docs += 1
        word = line.split()
        doc_len_dict[word[0]] = int(word[1])
        total_doc_len += int(word[1])

    print("Doc length",total_doc_len)
    print("Num of docs",num_of_docs)
    avg_doc_len = float(total_doc_len)/num_of_docs
    print("Average len",float(total_doc_len)/num_of_docs)

#retrieving word and its frequency from the index
def read_index_term_fre():
    f = open(_key_freq_file,'r')
    for line in f:
        word = line.split()
        if len(word) != 2:
            continue
        index_term_freq[word[0]] = int(word[1])


def read_final_index(file):
    f= open(file, 'r')
    cnt = 0
    for line in f:
        cnt += 1
        if cnt % 50000 == 0:
            print cnt
        temp_dict = {}
        word = line.split()
        if len(word) != 2:
            continue
        w = word[1].split(':')
        for d in w:
            c = d.split(',')
            temp_dict[c[0]] = int(c[1])
        final_index[word[0]] = temp_dict


#parameters for computation of bm25    
k1 = 1.2
k2 = 100
b = 0.75
ri = 0.0
R = 0.0

#compute the bm25 score
def compute_bm_25(q, qf, bm_25_dict, uids):
    if final_index.has_key(q):
        for doc_id, df in final_index[q].iteritems():
            if doc_id not in uids:
                continue
            avdl = float((doc_len_dict[doc_id]) / avg_doc_len)
            k = k1*((1-b)+b*avdl)
            score = (math.log(float(num_of_docs - index_term_freq[q] + 0.5)/(index_term_freq[q]+0.5)))*(((k1+1)*df)/(k+df))*(((k2+1)*qf)/(k2+qf))
            if bm_25_dict.has_key(doc_id) and bm_25_dict[doc_id] != -1000:
                bm_25_dict[doc_id] += score
            else:
                bm_25_dict[doc_id] = score


#read queries from query file 
def read_queries(queryfile):
    f = open(queryfile, 'r')
    f1 = open(_result_file, 'w')

    for line in f:
        attr = line.strip().split('\t')
        qid = attr[0]
        query = attr[1]
        uids = attr[2].split()
        bm_25_dict = {}
        for uid in uids:
            bm_25_dict[uid] = -1000
        query_dict = {}
        word = query.split(' ')
        # word = jieba.cut(query)

        for w in word:
            # w = w.encode('utf-8', 'ignore')
            if query_dict.has_key(w):
                query_dict[w] += 1
            else:
                query_dict[w] = 1
        for k, v in query_dict.items():
            compute_bm_25(k, v, bm_25_dict, uids)
        for uid in bm_25_dict:
            f1.write(str(qid)+"\t"+str(uid)+"\t"+str(bm_25_dict[uid])+"\n")

        
if __name__ == "__main__":

    newfile = _index_file
    queryfile = _queries_file
    read_final_index(newfile)
    print 'read_final_index done!'
    cal_doc_len()
    print 'cal_doc_len done!'
    read_index_term_fre()
    print 'read_index_term_fre done!'
    read_queries(queryfile)
    print 'all done!'
