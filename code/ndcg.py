import sys
import random
import numpy as np
import math


def top_k(y_true, y_pred, rel_threshold=0., k=10):
    if k <= 0.:
        return 0.
    s = 0.
    y_true = np.squeeze(y_true)
    y_pred = np.squeeze(y_pred)
    c = zip(y_true, y_pred)
    random.shuffle(c)
    c_g = sorted(c, key=lambda x: x[0], reverse=True)
    c_p = sorted(c, key=lambda x: x[1], reverse=True)
    idcg = 0.
    ndcg = 0.
    for i, (g, p) in enumerate(c_g):
        if i >= k:
            break
        if g > rel_threshold:
            # idcg += (math.pow(2., g) - 1.) / math.log(2. + i)
            idcg += g / math.log(2. + i) # * math.log(2.)
    for i, (g, p) in enumerate(c_p):
        if i >= k:
            break
        if g > rel_threshold:
            # ndcg += (math.pow(2., g) - 1.) / math.log(2. + i)
            ndcg += g / math.log(2. + i) # * math.log(2.)
    if idcg == 0.:
        return 0.
    else:
        return ndcg / idcg


def cal_ndcg(file_path, num=10, isRandom=False):
    rank_list = {}

    with open(file_path) as file:
        for line in file:
            qid, uid, rel, score = line.strip().split('\t')
            rel = float(rel)
            score = float(score)
            if qid not in rank_list:
                rank_list[qid] = []
            rank_list[qid].append([rel, score])

    idea_list = {}
    my_list = {}
    for qid in rank_list:
        # idea_list[qid] = sorted(rank_list[qid], key=lambda x:x[0], reverse=True)
        # my_list[qid] = sorted(rank_list[qid], key=lambda x:x[1], reverse=True)
        idea_list[qid] = []
        my_list[qid] = []
        for rel, score in rank_list[qid]:
            idea_list[qid].append(rel)
            my_list[qid].append(score)
            # idea_list[qid] = tmp
            # tmp = []
            # for i in my_list[qid]:
            #     tmp.append(i[0])
            # my_list[qid] = tmp

    # isRandom = True  # False


    ndcg_list = []
    for i in range(num):
        results = 0.
        for qid in rank_list:
            if isRandom:
                my_list[qid] = []
                for j in range(len(rank_list[qid])):
                    my_list[qid].append(random.random())
            # if qid != '0030':
            #    continue
            # random.shuffle(rank_list[qid])
            # print idea_list[qid]
            # print rank_list[qid]
            # print ''
            results_qid = top_k(y_true=idea_list[qid], y_pred=my_list[qid], k=10)
            # print qid, results_qid
            results += results_qid
        # sum += results
        # print results
        ndcg = results / len(rank_list)
        ndcg_list.append(ndcg)
        # print ndcg
    print 'ndcg@10 mean:', np.round(np.mean(ndcg_list), 5), ', std:', np.round(np.std(ndcg_list), 5)
