# coding: utf8


from bs4 import BeautifulSoup
from bootstrap import *
from common import *
import random
import re
import os
import io
import logging


class Tags(object):
    """
    遍历年份标签下所有有用的页面。
    遍历该年份完成后在对应的 cache/tags/year 目录下生成一个 done 文件。说明该标签已处理完毕
    """

    def __init__(self, year):
        self.start = 0
        self.step = 15
        self.flag = True
        self.pattern = re.compile(r'^http[s]?://movie.douban.com/subject/\d+', )
        self.retry_set = set()
        self.year = int(year)
        self.templete = 'https://www.douban.com/tag/%d/movie?start={start}' % self.year
        self.douban_url = ''
        self.basepath = './cache/tags/{year}/'.format(year=self.year)
        self.resultpath = tag_result_path
        self.done_filepath = self.basepath + 'done.txt'

    def get_url(self):
        self.douban_url = self.templete.format(start=self.start)
        self.start += self.step
        return self.douban_url

    def do(self, douban_url):
        # cache/tags/1888/f/f9751de431104b125f48dd79cc55822a
        m.update(douban_url)
        md5 = m.hexdigest()
        start_dir = md5[:1]
        dir_name = self.basepath + "{start}/".format(start=start_dir)
        file_path = dir_name + md5 + '.html'
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)

        if os.path.isfile(file_path):
            logging.debug('read html file from cache. filepath: {filepath}'.format(filepath=file_path))
            with open(file_path, 'r') as fr:
                html = fr.read()
        else:
            logging.debug('read html file from network. douban_url: {douban_url}'.format(douban_url=douban_url))
            rsp = http_get(douban_url)
            if rsp.status_code != 200:
                self.retry_set.add(douban_url)
                logging.debug('douban_url: {0} status_code: {1}'.format(douban_url, rsp.status_code))
                return False
            html = unicode(clean_html(rsp.text))
            with io.open(file_path, 'w', encoding='utf-8') as subject_fw:
                subject_fw.write(html)
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.find_all('a', class_='title')
        temp = []
        for item in results:
            if item.has_attr('href') and re.match(self.pattern, item['href']):
                temp.append(item['href'])
        if not temp:
            logging.debug('can not match a tag')
            logging.debug(results)
            self.flag = False
        return temp

    def save(self, results):
        if not os.path.isdir(self.resultpath):
            os.makedirs(self.resultpath)
        file_path = self.resultpath + '{year}.txt'.format(year=self.year)
        result_fw = io.open(file_path, 'w', encoding='utf-8')
        for item in results:
            result_fw.write(unicode(item + '\n'))
        result_fw.close()

        # 保存一个 done 文件
        with io.open(self.done_filepath, 'w', encoding='utf-8') as done_fw:
            done_fw.write(unicode('done' + '\nLast url:\n' + self.douban_url))

    def work(self):
        if os.path.isfile(self.done_filepath):
            logging.debug('the {year} tag is already catch done'.format(year=self.year))
            return
        result = []
        while self.flag:
            douban_url = self.get_url()
            logging.debug(douban_url)
            results = self.do(douban_url)
            if not results:
                logging.debug('douban_url: {douban_url} can not find $("a.title") ')
                self.flag = False
                continue
            result += results

        # retry
        for douban_url in self.retry_set:
            results = self.do(douban_url)
            if results:
                result += results

        self.save(result)


class Subject(object):
    def __init__(self, douban_url):
        self.douban_url = douban_url
        self.bashpath = subject_path
        pattern = r'http[s]?://movie.douban.com/subject/(\d+)'
        tmp = re.match(pattern, douban_url)
        if tmp and tmp.groups() and len(tmp.groups()) > 0:
            self.id = tmp.groups()[0]
        else:
            self.id = random.randint(1, 100)
        self.path = self.bashpath + str(self.id)[-1] + '/'
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        self.filepath = self.path + str(self.id) + '.html'

    def work(self):
        if os.path.isfile(self.filepath):
            logging.debug('subject file exists. path: {path}'.format(path=self.filepath))
            return
        rsp = self.get()
        if rsp:
            self.save(rsp)

    def get(self):
        rsp = http_get(self.douban_url)
        if rsp.status_code == 200:
            return rsp.text
        elif rsp.status_code == 404:
            pass
        else:
            logging.warning('url: {url} status_code: {code}'.format(url=self.douban_url, code=rsp.status_code))
            logging.warning('request headers:')
            logging.warning(rsp.request.headers)
            logging.warning('response: ')
            logging.warning(rsp.headers)
            logging.warning(rsp.text)

    def save(self, html):
        html = unicode(clean_html(html))
        with io.open(self.filepath, 'w', encoding='utf-8') as file_w:
            file_w.write(html)
        subjects_result_fw.write(html + '\n')


class Parser(object):
    def __init__(self):
        self.html = ''
        self.soup = ''


    def set_html(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, 'lxml')


    def run(self):
        result = {}

        # 原始链接地址
        source_url = self.soup.find('a', class_='bn-sharing')
        if source_url and 'data-url' in source_url.attrs:
            result['source_url'] = source_url.attrs['data-url']
        else:
            result['source_url'] = ''

        # 电影标题和上映年份
        head = self.soup.select('div#content h1 span')
        if len(head) <= 0:
            raise ValueError('{0} Head list at least have one element(movie title). Commonly, it has two elements,'
            'one is title, another is movie published year'.format(result['source_url']))
        result['title'] = head[0].get_text()
        if len(head) > 1:
            result['year'] = head[1].get_text()[1:-1]       # 示例：(2004)，去除前后括号
        else:
            result['year'] = 0

        # 评分
        rating_num = self.soup.select('div#interest_sectl div.rating_self strong.rating_num')
        if len(rating_num) < 0:
            raise ValueError('{0} can not find rating num'.format(result['source_url']))
        result['rating_num'] = rating_num[0].get_text()

        # 简介
        intro = self.soup.find('div', id='link-report')
        if not intro:
            result['intro'] = ''
            # raise ValueError('{0} can not find introduce'.format(result['source_url']))
        else:
            result['intro'] = intro.get_text(strip=True).replace(u'©豆瓣', '')

        # 电影数据，包括：导演、编剧、主演、类型、制片国家、语言、上映日期、片长、别名和IMDB链接
        subject = self.soup.select('#content div.article div.indent.clearfix div.subject.clearfix')
        if len(subject) < 0:
            raise ValueError('{0} can not find movie subject'.format(result['source_url']))
        subject = subject[0]
        cover = subject.find('img')
        if cover and cover.has_attr('src'):
            result['cover'] = cover.attrs['src']
        else:
            result['cover'] = ''
        info = subject.select('div#info')
        if len(info) < 0:
            raise ValueError('{0} can not find movie infomation'.format(result['source_url']))
        info_text = info[0].get_text()
        l = [x for x in info_text.split('\n') if len(x)>0]
        map = (
            (u'导演: ', 'director'),
            (u'编剧: ', 'playwright'),
            (u'主演: ', 'actors'),
            (u'类型: ', 'type'),
            (u'制片国家/地区: ', 'regon'),
            (u'语言: ', 'language'),
            (u'上映日期: ', 'date'),
            (u'片长: ', 'movie_length'),
            (u'又名: ', 'alias'),
            (u'IMDb链接: ', 'imdb_link'),
        )
        for i in l:
            for m in map:
                if re.match(m[0], i):
                    result[m[1]] = i.replace(m[0], '')

        return result
