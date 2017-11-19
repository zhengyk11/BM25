# merge key_freq

word_freq_dict = {}

file = open('key_freq_1.txt', 'r')
for line in file:
    line = line.strip()
    attr = line.split(' ')
    if len(attr) != 2:
        continue
    word = attr[0].strip().decode('utf-8', 'ignore').encode('utf-8', 'ignore')
    freq = int(attr[1])
    word_freq_dict[word] = freq
    # if word not in word_freq_dict:
    #     word_freq_dict[word] = freq
    # else:
    #     word_freq_dict[word] += freq
file.close()
print len(word_freq_dict)

file = open('key_freq_50_test_title.txt', 'r')
for line in file:
    line = line.strip()
    attr = line.split(' ')
    if len(attr) != 2:
        continue
    word = attr[0].strip().decode('utf-8', 'ignore').encode('utf-8', 'ignore')
    freq = int(attr[1])
    # word_freq_dict[word] = freq
    if word not in word_freq_dict:
        word_freq_dict[word] = freq
    else:
        word_freq_dict[word] += freq
file.close()
print len(word_freq_dict)

output = open('key_freq_50_test_title.txt', 'w')
for w in word_freq_dict:
    output.write(w+' '+str(word_freq_dict[w])+'\n')
output.close()