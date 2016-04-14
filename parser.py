# coding: utf8

from __future__ import print_function
from package.library import Parser
from package.bootstrap import subjects_result, subject_path
import json
import os
import io


if __name__ == '__main__':
    parser = Parser()

    if not os.path.isfile(subjects_result):
        print('Need parse file named: {0}'.format(subjects_result))
        exit()

    fw = io.open('output.data', 'w', encoding='utf-8')
    for line in open(subjects_result, 'r'):
        if not str(line).strip():
            continue
        parser.set_html(line)
        html = parser.run()
        # you can format the html dict, and output it
        # I like json, so I output json result
        fw.write(unicode(json.dumps(html)) + '\n')
    fw.close()
