# coding=utf-8
__author__ = "alvin"
__date__ = "2018/4/3 15:59"
import hashlib
import re


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def rm_html_tags(content):
    article = content[0]
    dr = re.compile(r'<[^>]+>', re.S)
    return dr.sub('', article)


if __name__ == "__main__":
    print(get_md5(b"https://www.baidu.com"))