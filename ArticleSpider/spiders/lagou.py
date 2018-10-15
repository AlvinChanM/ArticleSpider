# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ArticleSpider.items import LagouJobItemLoader, LagouJobItem

from ArticleSpider.utils.common import get_md5

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    # 从start_url开始，对每一个url发起请求
    start_urls = ['https://www.lagou.com/']
    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 1,
        'DEFAULT_REQUEST_HEADERS': {
            'Cookie': '_ga=GA1.2.794309225.1523366119; _gid=GA1.2.429231507.1523366119; user_trace_token=20180410211519-37ca3e62-3cc1-11e8-b743-5254005c3644; LGUID=20180410211519-37ca42a3-3cc1-11e8-b743-5254005c3644; JSESSIONID=ABAAABAACBHABBICB77ED386FC14711166841D709BEC346; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1523366119,1523366429,1523420179; SEARCH_ID=854c55dada764172bb5a0b9168f107af; TG-TRACK-CODE=jobs_code; X_HTTP_TOKEN=4167aefc733146dfcbba545569e8e7b9; _gat=1; LGSID=20180411201546-1041509f-3d82-11e8-b98d-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fts%3D1523448945686%26serviceId%3Dlagou%26service%3Dhttps%25253A%25252F%25252Fwww.lagou.com%25252F%26action%3Dlogin%26signature%3DDD2BC30C7C2D3D2F8C163815AF7E8737; LG_LOGIN_USER_ID=9f20e4c16b2d4510b0d85029d16771c17f20cc175c337232; _putrc=83689D67BBF198FA; login=true; unick=%E9%99%88%E8%8B%97; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=49; gate_login_token=71f89a9a779ab3c62dcaf06b33d8d3a7e4e7130849cc3c7d; index_location_city=%E4%B8%8A%E6%B5%B7; LGRID=20180411201557-171db0cf-3d82-11e8-b746-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1523448957',
        }
    }
    # 过滤url，缩小请求范围
    rules = (
        Rule(LinkExtractor(allow=("zhaopin/.*",)), follow=True),
        Rule(LinkExtractor(allow=("gongsi/j\d+.html",)), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )

    # def parse_start_url(self, response):
    #     return []
    #
    # def process_results(self, response, results):
    #     return results

    def parse_job(self, response):
        # 解析拉勾网的职位
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css("title", ".job-name::attr(title)")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("salary", ".salary::text")
        item_loader.add_xpath("job_city", '//*[@class="job_request"]/p/span[2]/text()')
        item_loader.add_xpath("work_years", '//*[@class="job_request"]/p/span[3]/text()')
        item_loader.add_xpath("degree_need", '//*[@class="job_request"]/p/span[4]/text()')
        item_loader.add_xpath("job_type", '//*[@class="job_request"]/p/span[5]/text()')
        item_loader.add_css("tags", '.position-label li::text')
        item_loader.add_css("publish_time", '.publish_time::text')
        item_loader.add_css("job_advantage", '.job-advantage p::text')
        item_loader.add_css("job_desc", '.job_bt div')
        item_loader.add_css("job_addr", '.work_addr')
        item_loader.add_css("company_name", '#job_company dt a img::attr(alt)')
        item_loader.add_css("company_url", '#job_company dt a::attr(href)')
        item_loader.add_value("crawl_time", datetime.now())

        job_item = item_loader.load_item()

        return job_item


