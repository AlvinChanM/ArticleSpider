# -*- coding: utf-8 -*-
import requests
import re

import scrapy
from urllib import parse
from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5
from scrapy.http import Request
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class JobboleSpider(scrapy.Spider):
    # custom_settings = {
    #                     'JOBDIR': 'job_info/001',
    #                     }
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    # def __init__(self):
    #     self.browser = webdriver.Chrome(executable_path=r'D:/virtualenv/chromedriver.exe')
    #     super(JobboleSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self, spider):
    #     # 当爬虫结束，关闭chrome
    #     print("spider closed!")
    #     self.browser.quit()

    # 设置伯乐在线所有404的url以及404页面数
    # handle_http_status_list = [404]
    #
    # def __init__(self):
    #     self.fail_urls = []
    #     dispatcher.connect(self.handle_spider_closed, signals.spider_closed)
    #
    # def handle_spider_closed(self, spider, reason):
    #     self.crawler.stats.set_value("failed_urls", ",".join(self.fail_urls))


    def parse(self, response):
        """
        1. 获取文章列表页中的文章url进行拼接并回调给parse_detail获取详情
        2. 获取下一页的url进行拼接，并回调自己本身

        """
        # if response.status == 404:
        #     self.fail_urls.append(response.url)
        #
        #     self.crawler.stats.inc_value("failed_url")
        # 获取该文章所在的节点
        post_nodes = response.css(".post.floated-thumb .post-thumb a")
        # 获取文章的URL和IMAGE
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first()
            post_url = post_node.css("::attr(href)").extract_first()
            # URL拼接及获取详情页
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)

        # 提取该URL中的下一页URL，并调用自己本身，来获取所有文章的URL和详情
        next_url = response.css("a.next.page-numbers::attr(href)").extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
        # pass

    # 获取详情
    def parse_detail(self, response):
        # article_item = JobBoleArticleItem()
        # # 通过xpath爬取字段
        # # 文章封面图

        front_image_url = response.meta.get("front_image_url", "")
        # # 文章标题
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
        # # 文章日期
        # create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first("").strip(
        #
        # ).replace(
        #     '·', '').strip()
        # # 文章评论数
        # comment_num_str = response.css('a[href*="comment"] span::text').extract_first("")
        # comment_num = re.match(r'.*?(\d+).*', comment_num_str)
        # if not comment_num:
        #     comment_num = 0
        # else:
        #     comment_num = int(comment_num.group(1))
        # # 文章分享数
        share_api = 'http://i.jiathis.com/url/shares.php?url={post_url}#article-comment'.format(post_url=response.url)
        share_num_str = requests.get(share_api).text
        share_num = int(re.match(r'.*?(\d+).*', share_num_str).group(1))
        # # 文章点赞数
        # praise_num = int(response.css('div.post-adds span h10::text').extract_first(""))
        # # 文章收藏数
        # fav_num_str = response.css(".post-adds span.bookmark-btn::text").extract_first("")
        # fav_num = re.match(r'.*?(\d+).*', fav_num_str)
        # # 如果取不到收藏数
        # if not fav_num:
        #     fav_num = 0
        # else:
        #     fav_num = int(fav_num.group(1))
        # # 获取文章
        # article = response.css('.entry').extract_first()
        # dr = re.compile(r'<[^>]+>', re.S)
        # content = dr.sub('', article)
        #
        # # tag
        # tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # tags = [tag for tag in tag_list if not tag.strip().endswith("评论")]
        # tag = ",".join(tags)
        # # 实例化item
        # article_item["url_object_id"] = get_md5(response.url)
        # article_item["title"] = title
        # try:
        #     create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # article_item["create_date"] = create_date
        # article_item["url"] = response.url
        # article_item["content"] = content
        # # 下载图片是地址必须是list
        # article_item["front_image_url"] = [front_image_url]
        # article_item["praise_num"] = praise_num
        # article_item["fav_num"] = fav_num
        # article_item["share_num"] = share_num
        # article_item["comment_num"] = comment_num
        # article_item["tags"] = tag

        # 通过item loader加载item
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_value("share_num", share_num)
        item_loader.add_css("fav_num", ".post-adds span.bookmark-btn::text")
        item_loader.add_css("praise_num", "div.post-adds span h10::text")
        item_loader.add_css("comment_num", 'a[href*="comment"] span::text')
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")

        # 对item_loader进行解析
        article_item = item_loader.load_item()

        yield article_item







