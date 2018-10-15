# coding=utf-8
__author__ = "alvin"
__date__ = "2018/4/18 11:36"
from selenium import webdriver

browser = webdriver.Chrome(executable_path=r'D:/virtualenv/chromedriver.exe')
browser.get("https://www.zhihu.com/signup?next=%2F")
browser.find_element_by_css_selector(".SignContainer-switch span").click()
browser.find_element_by_css_selector(".SignFlow-accountInput input[name='username']").send_keys('18217379634')
browser.find_element_by_css_selector(".Input-wrapper input[name='password']").send_keys('miao920304?')
browser.find_element_by_css_selector("form.SignFlow button[type='submit']").click()


# t_selector = Selector(text=browser.page_source)
# print(t_selector.css('#self::text').extract())
# browser.quit()