from bm25 import *
from indexer import *
from merge import *
import json
from ndcg import *

# import argparse
#
# main_parser = argparse.ArgumentParser()
# main_parser.add_argument("--config", type=str)
# args = main_parser.parse_args()
#
# if not args.config:
#     exit(0)
#
# with open(args.config) as file:
#     config = json.load(file)

if __name__ == '__main__':
    # config = """
    # {
    #     "content_file": "../data/50_test_title/50_test_title_seg.txt",
    #     "content_file_2": "../data/50_test_title/50_test_title_seg.txt",

    #     "doc_length_file": "../data/doc_length/doc_length_click.txt",
    #     "doc_length_file_2": "../data/doc_length/doc_length.txt",
    #     "doc_length_file_merge": "../data/doc_length/doc_length_click_merge.txt",

    #     "doc_freq_file": "../data/doc_freq/doc_freq_click.txt",
    #     "doc_freq_file_2": "../data/doc_freq/doc_freq.txt",
    #     "doc_freq_file_merge": "../data/doc_freq/doc_freq_click_merge.txt",

    #     "index_file": "../data/index/index_click.txt",

    #     "qrel_file": "../data/50_test_title/50_test_qrels.txt",
    #     "qid_file": "../data/50_test_title/50_test_qid_seg.txt",
    #     "queries_file": "../data/queries/queries_click.txt",

    #     "result_file": "../results/bm25_results_click.txt"
    # }
    # """

    config = """
    {
        "content_file": "/home/luocheng/zhengyukun/collect_data_click_model_20171112/html2fulltext/fulltext_seg_filter_all.txt",

        "doc_length_file": "../data/doc_length/doc_length_click.txt",

        "doc_freq_file": "../data/doc_freq/doc_freq_click.txt",

        "index_file": "../data/index/index_click.txt",

        "qrel_file": "/home/luocheng/fanzhen/SogouData/time_data_small/all.TCM.DBN.PSCM.TPSCM.UBM.model.relevance.txt",
        "qid_file": "/home/luocheng/zhengyukun/collect_data_click_model_20171112/html2fulltext/click_qid_seg.txt",
        "queries_file": "../data/queries/queries_click.txt",

        "result_file": "../results/bm25_results_click.txt"
    }
    """

    config = json.loads(config)
    print(json.dumps(config, indent=2))

    # print '[Main] buiding...'
    # build(config['content_file'], config['doc_length_file'], config['doc_freq_file'], config['index_file'], isIndex=True)
    # build(config['content_file_2'], config['doc_length_file_2'], config['doc_freq_file_2'])

    # print '[Main] make_queries...'
    # make_queries(config['content_file'], config['qrel_file'], config['qid_file'], config['queries_file'])

    # print '[Main] merging...'
    # merge_doc_len([config['doc_length_file'], config['doc_length_file_2']], config['doc_length_file_merge'])
    # merge_doc_freq([config['doc_freq_file'], config['doc_freq_file_2']], config['doc_freq_file_merge'])

    print '[Main] calculating BM25 scores...'
    BM25(config['doc_freq_file'], config['doc_length_file'], config['index_file'], config['queries_file'], config['result_file'])










