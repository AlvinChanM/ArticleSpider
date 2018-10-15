# coding=utf-8
__author__ = "alvin"
__date__ = "2018/4/18 18:19"
from selenium import webdriver

# phantomjs.无界面浏览器，多进程情况下phantomjs的性能下降很严重
browser = webdriver.PhantomJS(executable_path="E:/home/phantomjs-2.1.1-windows/bin/phantomjs.exe")
browser.get("https://detail.tmall.com/item.htm?spm=a230r.1.14.3.yYBVG6&id=538286972599&cm_id=140105335569ed55e27b&abbucket=15&sku_properties=10004:709990523;5919063:6536025")

print (browser.page_source)
browser.quit()