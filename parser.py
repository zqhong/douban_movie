# coding: utf8

from __future__ import print_function
from package.library import Parser
from package.bootstrap import subject_path
import argparse
import json


if __name__ == '__main__':
    parser = Parser()
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--file', help='what file you want to parse', default=subject_path + 'subjects.data', type=str)
    args = arg_parser.parse_args()

    for line in open(args.file, 'r'):
        if not str(line).strip():
            continue
        parser.set_html(line)
        html = parser.run()
        # you can format the html dict, and output it
        # I like json, so I output json result
        print(json.dumps(html))
