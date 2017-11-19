#input
_1_doc_length_file = 'doc_length/doc_length.txt'
_1_index_file = 'index/indexer.out'
_1_key_freq_file = 'key_frep/key_freq.txt'

# suffix = '_50_test_title'
suffix = '_ntcir_small'

#output
_key_freq_file = 'key_frep/key_freq' + suffix + '.txt'
_doc_length_file = 'doc_length/doc_length' + suffix + '.txt'
_index_file = 'index/index' + suffix + '.out'
_queries_file = 'queries/queries' + suffix + '.txt'


def merge_doc_len():
    uid_length_dict = {}
    file = open(_1_doc_length_file, 'r')
    for line in file:
        line = line.strip()
        attr = line.split(' ')
        if len(attr) != 2:
            continue
        uid = attr[0].strip()
        length = int(attr[1])
        uid_length_dict[uid] = length

    file.close()
    print len(uid_length_dict)

    file = open(_doc_length_file, 'r')
    for line in file:
        line = line.strip()
        attr = line.split(' ')
        if len(attr) != 2:
            continue
        uid = attr[0].strip()
        length = int(attr[1])
        uid_length_dict[uid] = length

    file.close()
    print len(uid_length_dict)

    output = open(_doc_length_file, 'w')
    for uid in uid_length_dict:
        output.write(uid + ' ' + str(uid_length_dict[uid]) + '\n')
    output.close()

def merge_index():
    word_index_dict = {}
    file = open(_1_index_file, 'r')
    for line in file:
        line = line.strip()
        attr = line.split(' ')
        if len(attr) != 2:
            continue
        word = attr[0].strip().decode('utf-8', 'ignore').encode('utf-8', 'ignore')
        index = attr[1].strip()
        word_index_dict[word] = index
    file.close()
    print len(word_index_dict)

    file = open(_index_file, 'r')
    for line in file:
        line = line.strip()
        attr = line.split(' ')
        if len(attr) != 2:
            continue
        word = attr[0].strip().decode('utf-8', 'ignore').encode('utf-8', 'ignore')
        index = attr[1].strip()
        if word not in word_index_dict:
            word_index_dict[word] = index
        else:
            word_index_dict[word] += ':' + index
    file.close()
    print len(word_index_dict)

    output = open(_index_file, 'w')
    for w in word_index_dict:
        output.write(w + ' ' + str(word_index_dict[w]) + '\n')
    output.close()

def merge_key_freq():
    # merge key_freq
    word_freq_dict = {}

    file = open(_1_key_freq_file, 'r')
    for line in file:
        line = line.strip()
        attr = line.split(' ')
        if len(attr) != 2:
            continue
        word = attr[0].strip().decode('utf-8', 'ignore').encode('utf-8', 'ignore')
        freq = int(attr[1])
        word_freq_dict[word] = freq

    file.close()
    print len(word_freq_dict)

    file = open(_key_freq_file, 'r')
    for line in file:
        line = line.strip()
        attr = line.split(' ')
        if len(attr) != 2:
            continue
        word = attr[0].strip().decode('utf-8', 'ignore').encode('utf-8', 'ignore')
        freq = int(attr[1])

        if word not in word_freq_dict:
            word_freq_dict[word] = freq
        else:
            word_freq_dict[word] += freq
    file.close()
    print len(word_freq_dict)

    output = open(_key_freq_file, 'w')
    for w in word_freq_dict:
        output.write(w + ' ' + str(word_freq_dict[w]) + '\n')
    output.close()


if __name__ == '__main__':
    merge_doc_len()
    merge_index()
    merge_key_freq()
    print 'done!'