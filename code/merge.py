import re


def merge_doc_len(inputs, output):
    uid_length_dict = {}
    for input in inputs:
        with open(input, 'r') as file:
            for line in file:
                attr = re.split('[\t ]+', line.strip())
                if len(attr) != 2:
                    continue
                uid = attr[0].strip()
                length = int(attr[1])
                uid_length_dict[uid] = length

    print 'uid_length_dict', len(uid_length_dict)

    with open(output, 'w') as file:
        for uid in uid_length_dict:
            file.write(str(uid) + '\t' + str(uid_length_dict[uid]) + '\n')


def merge_index(inputs, output):
    word_index_dict = {}
    for input in inputs:
        with open(input, 'r') as file:
            for line in file:
                attr = re.split('[\t: ]+', line.strip())
                if len(attr) < 2:
                    continue
                word = attr[0].strip().lower() # .decode('utf-8', 'ignore').encode('utf-8', 'ignore')
                index = attr[1:]
                if word not in word_index_dict:
                    word_index_dict[word] = []
                word_index_dict[word] += index

    print 'word_index_dict', len(word_index_dict)

    with open(output, 'w') as file:
        for w in word_index_dict:
            file.write('%s\t%s\n' % (w, ':'.join(word_index_dict[w])))


def merge_doc_freq(inputs, output):
    word_freq_dict = {}

    for input in inputs:
        with open(input, 'r') as file:
            for line in file:
                attr = re.split('[\t ]+', line.strip())
                if len(attr) != 2:
                    continue
                word = attr[0].strip().lower()  # .decode('utf-8', 'ignore').encode('utf-8', 'ignore')
                freq = int(attr[1])
                if word not in word_freq_dict:
                    word_freq_dict[word] = 0
                word_freq_dict[word] += freq

    print 'word_freq_dict', len(word_freq_dict)

    with open(output, 'w') as file:
        for w in word_freq_dict:
            file.write('%s\t%d\n' % (w, word_freq_dict[w]))


# if __name__ == '__main__':
#     root_dir = '../data/'
#     _1_doc_length_file = root_dir + 'doc_length/doc_length.txt'
#     _1_index_file = root_dir + 'index/indexer.txt'
#     _1_doc_freq_file = root_dir + 'doc_freq/doc_freq.txt'
#
#     suffix = '_50_test_title'
#     # suffix = '_ntcir_small'
#
#     # output
#
#     _doc_length_file = root_dir + 'doc_length/doc_length' + suffix + '.txt'
#     _index_file = root_dir + 'index/index' + suffix + '.txt'
#     _doc_freq_file = root_dir + 'doc_freq/doc_freq' + suffix + '.txt'
#     _queries_file = root_dir + 'queries/queries' + suffix + '.txt'
#
#     merge_doc_len([_doc_length_file, _1_doc_length_file], _doc_length_file[:-4]+'_out.txt')
#     merge_index([_index_file, _1_index_file], _index_file[:-4]+'_out.txt')
#     merge_doc_freq([_doc_freq_file, _1_doc_freq_file], _doc_freq_file[:-4]+'_out.txt')
#     print 'done!'