# coding=utf-8
__author__ = "alvin"
__date__ = "2018/3/30 12:59"
from scrapy.cmdline import execute
import sys
import os
a=os.path.dirname(__file__)
b=os.path.abspath(a)
# 当前文件所在路径
c=os.path.abspath(__file__)
# 当前文件所在的目录
d=os.path.dirname(os.path.abspath(__file__))
# 将当前文件目录加入系统模块路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "jobbole"])
execute(["scrapy", "crawl", "zhihu"])
# execute(["scrapy", "crawl", "lagou"])