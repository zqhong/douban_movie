# coding: utf8

from __future__ import print_function
from package.library import Parser
from package.bootstrap import subjects_result, subject_path
import json
import os


if __name__ == '__main__':
    parser = Parser()

    if not os.path.isfile(subjects_result):
        my_commond = "find {0} -name '*.html' | xargs awk 1 > {1}".format(subject_path, subjects_result)
        # print('run system commond: ' + my_commond)
        os.system(my_commond)

    if not os.path.isfile(subjects_result):
        print('Some commond only support *nix, please run this program on *nix.')
        exit()

    for line in open(subjects_result, 'r'):
        if not str(line).strip():
            continue
        parser.set_html(line)
        html = parser.run()
        # you can format the html dict, and output it
        # I like json, so I output json result
        print(json.dumps(html))
