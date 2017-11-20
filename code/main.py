from bm25 import *
from indexer import *
from merge import *
import json

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
    config = """
    {
        "content_file": "../data/50_test_title/50_test_title_seg.txt",

        "doc_length_file": "../data/doc_length/doc_length_50_test_title.txt",
        "doc_length_file_2": "../data/doc_length/doc_length.txt",
        "doc_length_file_merge": "../data/doc_length/doc_length_50_test_title_merge.txt",

        "doc_freq_file": "../data/doc_freq/doc_freq_50_test_title.txt",
        "doc_freq_file_2": "../data/doc_freq/doc_freq.txt",
        "doc_freq_file_merge": "../data/doc_freq/doc_freq_50_test_title_merge.txt",

        "index_file": "../data/index/index_50_test_title.txt",
        "index_file_2": "../data/index/indexer.txt",
        "index_file_merge": "../data/index/index_50_test_title_merge.txt",

        "qrel_file": "../data/50_test_title/50_test_qrels.txt",
        "qid_file": "../data/50_test_title/50_test_qid_seg.txt",
        "queries_file": "../data/queries/queries_50_test_title.txt",

        "result_file": "../results/bm25_results__50_test_title.txt"
    }
    """
    config = json.loads(config)
    print(json.dumps(config, indent=2))

    build(config['content_file'], config['doc_length_file'], config['doc_freq_file'], config['index_file'])
    make_queries(config['content_file'], config['qrel_file'], config['qid_file'], config['queries_file'])

    merge_doc_len([config['doc_length_file'], config['doc_length_file_2']], config['doc_length_file_merge'])
    merge_index([config['index_file'], config['index_file_2']], config['index_file_merge'])
    merge_doc_freq([config['doc_freq_file'], config['doc_freq_file_2']], config['doc_freq_file_merge'])

    BM25(config)