# coding: utf8

from gevent.pool import Pool
from gevent.queue import Queue
from gevent import monkey
from package.library import Tags, Subject
from package.bootstrap import tag_result_file, tag_result_path
import io
import gevent
import os
import argparse


if __name__ == '__main__':
    monkey.patch_all()

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--start', help='what year you want to start crawl', default=1888, type=int)
    arg_parser.add_argument('--end', help='what year you want to end crawl', default=2016, type=int)
    arg_parser.add_argument('--thread', help='thread num', default=25, type=int)
    args = arg_parser.parse_args()

    # 1. 收集 subject
    pool = Pool(args.thread)
    threads = []
    for x in xrange(args.start, args.end + 1):
        t = Tags(x)
        g = pool.spawn(t.work)
        threads.append(g)
    gevent.joinall(threads)

    if not os.path.isfile(tag_result_file):
        l = []
        for x in os.listdir(tag_result_path):
            url = tag_result_path + x
            r = [x.replace('\n', '') for x in open(url, 'r')]
            l += r
        l = set(l)
        fw = io.open(tag_result_file, 'w', encoding='utf-8')
        for x in l:
            fw.write(unicode(x + '\n'))
        fw.close()

    # 2. 访问并保存 subject
    q = Queue()
    for x in open(tag_result_file, 'r'):
        q.put_nowait(str(x).replace('\n', ''))

    pool = Pool(args.thread)
    threads = []
    while not q.empty():
        url = q.get()
        s = Subject(url)
        t = pool.spawn(s.work)
        threads.append(t)
    gevent.joinall(threads)
