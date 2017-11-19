# merge key_freq

uid_length_dict = {}

file = open('doc_length_1.txt', 'r')
for line in file:
    line = line.strip()
    attr = line.split(' ')
    if len(attr) != 2:
        continue
    uid = attr[0].strip()
    length = int(attr[1])
    uid_length_dict[uid] = length
    # if word not in word_freq_dict:
    #     word_freq_dict[word] = freq
    # else:
    #     word_freq_dict[word] += freq
file.close()
print len(uid_length_dict)

file = open('doc_length_50_test_title.txt', 'r')
for line in file:
    line = line.strip()
    attr = line.split(' ')
    if len(attr) != 2:
        continue
    uid = attr[0].strip()
    length = int(attr[1])
    uid_length_dict[uid] = length
    # if word not in word_freq_dict:
    #     word_freq_dict[word] = freq
    # else:
    #     word_freq_dict[word] += freq
file.close()
print len(uid_length_dict)

output = open('doc_length_50_test_title.txt', 'w')
for uid in uid_length_dict:
    output.write(uid+' '+str(uid_length_dict[uid])+'\n')
output.close()