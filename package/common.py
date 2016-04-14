# coding: utf8

from urlparse import urlparse
from bootstrap import *
import re
import random
import requests
import string


def generate_headers(douban_url):
    return {
        'Referer': 'https://movie.douban.com/subject/{id}/?from=tag_all'.format(id=random.randint(1, 2291828)),
        'User-Agent': fake.user_agent(),
        'X-Forwarded-For': fake.ipv4(),
        'Accept-Encoding': 'gzip',
        'Cookie': 'bid={0}'.format(random_str(random.randint(11, 16))),
        'Host': urlparse(douban_url).netloc,
    }

def clean_html(html):
    """去除html页面中多余的 link、meta、script标签；去除换行符"""
    html = str(html)
    html = re.sub(r'<link.+>', '', html)
    html = re.sub(r'<meta.+>', '', html)
    html = re.sub(r'(?s)<script.+?</script>', '', html)
    html = re.sub(r'(?s)<style.+?</style>', '', html)
    html = html.replace('\n', '')
    return html

def random_str(str_len):
    return ''.join([random.choice(string.letters + string.digits) for _ in xrange(str_len)])


def http_get(douban_url):
    return requests.get(douban_url, headers=generate_headers(douban_url), verify=False)
