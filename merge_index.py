# merge key_freq

word_index_dict = {}

file = open('indexer_1.out', 'r')
for line in file:
    line = line.strip()
    attr = line.split(' ')
    if len(attr) != 2:
        continue
    word = attr[0].strip().decode('utf-8', 'ignore').encode('utf-8', 'ignore')
    index = attr[1].strip()
    word_index_dict[word] = index
    # if word not in word_freq_dict:
    #     word_freq_dict[word] = freq
    # else:
    #     word_freq_dict[word] += freq
file.close()
print len(word_index_dict)

file = open('indexer_50_test_title.out', 'r')
for line in file:
    line = line.strip()
    attr = line.split(' ')
    if len(attr) != 2:
        continue
    word = attr[0].strip().decode('utf-8', 'ignore').encode('utf-8', 'ignore')
    index = attr[1].strip()
    # word_freq_dict[word] = freq
    if word not in word_index_dict:
        word_index_dict[word] = index
    else:
        word_index_dict[word] += ':' + index
file.close()
print len(word_index_dict)

output = open('indexer_50_test_title.out', 'w')
for w in word_index_dict:
    output.write(w+' '+str(word_index_dict[w])+'\n')
output.close()
