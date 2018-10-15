# coding=utf-8
__author__ = "alvin"
__date__ = "2018/4/18 17:10"

import time
from selenium import webdriver
browser = webdriver.Chrome(executable_path=r'D:/virtualenv/chromedriver.exe')
browser.get("https://weibo.com")
time.sleep(7)
browser.find_element_by_css_selector("input[node-type='username']").send_keys("18217379634")
browser.find_element_by_css_selector(".info_list.password div.input_wrap input[type='password']").send_keys(
    "miao920304")
time.sleep(3)
browser.find_element_by_css_selector(".info_list.login_btn").click()
for i in range(3):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
    time.sleep(3)

