# coding: utf8

from faker import Factory
import logging
import hashlib
import os
import sys


reload(sys)
sys.setdefaultencoding('utf-8')


log_dir = './log/'
if not os.path.isdir(log_dir):
    os.makedirs(log_dir)
logging.basicConfig(filename=log_dir + 'spider.log', level=logging.DEBUG)
tag_result_path = './cache/tags/result/'
if not os.path.isdir(tag_result_path):
    os.makedirs(tag_result_path)
tag_result_file = tag_result_path + 'subjects.txt'
subject_path = './cache/subjects/'
subject_result_path = subject_path + 'result/'
if not os.path.isdir(subject_result_path):
    os.makedirs(subject_result_path)
fake = Factory.create('zh_CN')
m = hashlib.md5()
