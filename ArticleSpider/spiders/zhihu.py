# -*- coding: utf-8 -*-
import datetime
import json
import time

from ArticleSpider.settings import SQL_DATETIME_FORMAT
import scrapy
import re
from urllib import parse
from scrapy.http import Request
from ArticleSpider.items import ZhihuAnswerItem, ZhihuQuestionItem
from scrapy.loader import ItemLoader


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']
    # question的第一页anwser请求接口
    start_answer_url = 'https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B%2A%5D.is_normal' \
                       '%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail' \
                       '%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment' \
                       '%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission' \
                       '%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt' \
                       '%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp' \
                       '%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author' \
                       '.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}&sort_by=default'
    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 1,

        # 需要登录后的cookie验证
        'DEFAULT_REQUEST_HEADERS': {
            'Cookie': 'q_c1=bbe313be5f10409fac05a3894738446c|1522660227000|1522660227000; __DAYU_PP=3YuZ3vQfiJQqny2Ff7Fy3d6328efaf58; _zap=8ef1ed29-d303-4868-b67d-a519ecc89750; l_cap_id="YWNmMTlmYzkwYWIyNGQ4MThlOGNhNTQ2MjY0ZjdkYmQ=|1523277955|e8e2292c01122c5d76c0cf7ee640dac853299fd0"; r_cap_id="MDcxMzAwY2ViMGNiNDQ0NmIyNjBjNWQ0MDdjZDg0NzI=|1523277955|6803414603aafec44b3b7abf83df575cc4010ba1"; cap_id="ZTYyZjY0MTg1ZTMwNDAyYmIwYzUwM2ZkN2YzNDMyOTU=|1523277955|4b15e1ce026a7b33d5a67e501f2e5ccbd01e0b6e"; __utma=155987696.1818569290.1524910209.1524910209.1524910209.1; __utmz=155987696.1524910209.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); aliyungf_tc=AQAAACqncH8/5goAfLUB2u9LOS3ZZYLM; _xsrf=75f9118e-fec6-45eb-9d80-4fba7a793e72; d_c0="AMBvZfP0gw2PTlvLHumntIh9ArB9xZI7x4I=|1524973772"; capsion_ticket="2|1:0|10:1524975051|14:capsion_ticket|44:ODQ2ZmUxYjNiY2U5NDJiYTgxOTJlNDM3NDY0ODg5Yjg=|048117a06effb802933a3e201a5331830aec25fc5084c09df7a775ee4e7dbf5c"; z_c0="2|1:0|10:1524975064|4:z_c0|92:Mi4xVi1pTEF3QUFBQUFBd0c5bDhfU0REU1lBQUFCZ0FsVk4ySlBTV3dEamNXdDRyNUdCN08zTUY2WHU3eFZCTzN6U2FR|641b35e3fd1175149b6685f7f8456ceb7f1b09a8f9c459ea77d8871f61136a42"',
            'Host': 'www.zhihu.com',
            'Referer': 'https://www.zhihu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/64.0.3282.140 Safari/537.36',
            }
             }

    def parse(self, response):
        """
        提取出html中所有url，并跟踪这些url进行爬取，如果提取的url中格式为/question/xxx，就下载后直接进入解析函数
        """
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            match_url = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_url:
                # 如果匹配到question页面则下载后交由parse_detail进行解析
                request_url = match_url.group(1)
                question_id = match_url.group(2)
                # scrapy 通过yield把url提交给下载器
                yield scrapy.Request(request_url, meta={'question_id': question_id}, callback=self.parse_detail)
            else:
                # 如果匹配不到qustion页面，则继续匹配
                yield scrapy.Request(url, callback=self.parse)

    def parse_detail(self, response):
        # 从request_url 中提取question_item内容
        item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
        item_loader.add_css('title', '.QuestionHeader-title::text')
        item_loader.add_css('content', '.QuestionHeader-detail')
        item_loader.add_value('url', response.url)
        question_id = response.meta.get('question_id', '')
        item_loader.add_value('question_id', question_id)
        item_loader.add_css('answer_num', 'h4.List-headerText span::text')
        item_loader.add_css('click_num', '.NumberBoard-itemValue::attr(title)')
        item_loader.add_css('comment_num', '.QuestionHeader-Comment button::text')
        item_loader.add_css('watch_user_num', '.NumberBoard-itemValue::attr(title)')
        item_loader.add_css('topics', '.Popover div::text')
        item_loader.add_value('crawl_time', datetime.datetime.now().strftime(SQL_DATETIME_FORMAT))

        question_item = item_loader.load_item()
        yield scrapy.Request(url=self.start_answer_url.format(question_id, 20, 0), callback=self.parse_answer)
        yield question_item

    def parse_answer(self, response):
        # 处理question的answer
        answer_json = json.loads(response.text)
        is_end = answer_json["paging"]["is_end"]
        next_url = answer_json["paging"]["next"]

        # 提取answer内容
        for answer in answer_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item["answer_id"] = int(answer['id'])
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else "匿名作者"
            answer_item["content"] = answer["content"] if "content" in answer else "内容为空"
            answer_item["praise_num"] = int(answer["voteup_count"])
            answer_item["comment_num"] = int(answer["comment_count"])
            answer_item["update_time"] = time.strftime(SQL_DATETIME_FORMAT, time.localtime(answer["updated_time"]))
            answer_item["create_time"] = time.strftime(SQL_DATETIME_FORMAT, time.localtime(answer["created_time"]))
            answer_item["crawl_time"] = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

            yield answer_item
            pass

        if not is_end:
            yield scrapy.Request(next_url)

    def start_requests(self):
        return [scrapy.Request(url='https://www.zhihu.com/', callback=self.check_login)]

    def check_login(self, response):
        # 验证是否登录成功
        if response.url == 'https://www.zhihu.com/':

            for url in self.start_urls:
                yield Request(url, dont_filter=True)
        else:
            pass
