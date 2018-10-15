# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from elasticsearch_dsl.connections import connections

import datetime
import re

import redis
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
# 去除html标签的包
from w3lib.html import remove_tags
from ArticleSpider.settings import SQL_DATETIME_FORMAT

from ArticleSpider.utils.common import rm_html_tags
from ArticleSpider.models.es_types import ArticleType, ZhihuAnswerType, ZhihuQuestionType, LaGouType

# 连接到服务器
es_Ar = connections.create_connection(ArticleType._doc_type.using)
es_Q = connections.create_connection(ZhihuQuestionType._doc_type.using)
es_A = connections.create_connection(ZhihuAnswerType._doc_type.using)
es_L = connections.create_connection(LaGouType._doc_type.using)

redis_cli = redis.StrictRedis()


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def get_num(value):
    match = re.match(r'.*?(\d+).*', value)
    # 如果取不到收藏数
    if not match:
        num = 0
    else:
        num = int(match.group(1))
    return num


def get_comment_tags(value):
    # 去掉tag中的‘评论’
    if '评论' in value:
        return ""
    else:
        return value


def return_value(value):
    return value

def gen_suggests(index, info_tuple):
    #根据字符串生成搜索建议数组
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            #调用es的analyze接口分析字符串
            # words = es.indices.analyze(index=index, params={"filter": ["lowercase"]}, body=text)
            if index == ZhihuQuestionType._doc_type.index:
                words = es_Q.indices.analyze(index=index,  analyzer="ik_max_word", params={'filter': ["lowercase"]},
                                       body=text)
            elif index == ZhihuAnswerType._doc_type.index:
                words = es_A.indices.analyze(index=index, analyzer="ik_max_word", params={'filter': ["lowercase"]},
                                             body=text)
            elif index == LaGouType._doc_type.index:
                words = es_L.indices.analyze(index=index,  analyzer="ik_max_word", params={'filter': ["lowercase"]},
                                       body=text)
            else:
                words = es_Ar.indices.analyze(index=index,  analyzer="ik_max_word", params={'filter': ["lowercase"]},
                                       body=text)
            analyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            new_words = analyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})

    return suggests


class ArticleItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(input_processor=MapCompose(date_convert))
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    # 覆盖out_processor，保持原样输出
    front_image_url = scrapy.Field(output_processor=MapCompose(return_value))
    front_image_path = scrapy.Field()
    praise_num = scrapy.Field(input_processor=MapCompose(get_num))
    comment_num = scrapy.Field(input_processor=MapCompose(get_num))
    share_num = scrapy.Field()
    fav_num = scrapy.Field(input_processor=MapCompose(get_num))
    tags = scrapy.Field(input_processor=MapCompose(get_comment_tags), output_processor=Join(','))
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                    insert into jobbole(title,create_date,url,url_object_id,front_image_url,front_image_path
                    ,comment_num,fav_num,praise_num,share_num,content,tags)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)ON DUPLICATE KEY
                     UPDATE content=VALUES(content), tags=VALUES(tags), praise_num=VALUES(praise_num), fav_num=VALUES
                    (fav_num)
                    """
        params = (self['title'], self['create_date'], self['url'], self['url_object_id'],
                  self['front_image_url'], self['front_image_path'], self['comment_num'],
                  self['fav_num'], self['praise_num'], self['share_num'], self["content"],
                  self['tags']
                )
        return insert_sql, params

    def save_to_es(self):
        article = ArticleType()
        article.title = self["title"]
        article.create_date = self["create_date"]
        article.praise_num = self["praise_num"]
        article.share_num = self["share_num"]
        article.fav_num = self["fav_num"]
        article.url = self["url"]
        article.meta.id = self["url_object_id"]
        article.tags = self["tags"]
        article.content = remove_tags(self["content"])
        article.front_image_url = self["front_image_url"]
        article.comment_num = self["comment_num"]
        if "front_image_path" in self:
            article.front_image_path = self["front_image_path"]
        # article.suggest = gen_suggest(ArticleType._doc_type.index, ((article.title, 10), (article.tags, 7)))
        article.suggest = gen_suggests(ArticleType._doc_type.index, ((article.title, 10), (article.tags, 7)))
        article.save()

        redis_cli.incr("jobbole_count")

        return


class LagouJobItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()
    pass


def rm_slash(value):
    return value.replace("/", "")


def match_publish_time(value):
    return (re.match('(.*)\s.*', value).group(1)).strip()


def rm_space(value):
    return value.strip()


def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip() != "查看地图"]
    return "".join(addr_list)


class LagouJobItem(scrapy.Item):
    # 拉勾网职位信息
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    job_city = scrapy.Field(input_processor=MapCompose(rm_slash))
    work_years = scrapy.Field(input_processor=MapCompose(rm_slash))
    job_type = scrapy.Field()
    publish_time = scrapy.Field(input_processor=MapCompose(match_publish_time))
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field(input_processor=MapCompose(remove_tags, rm_space))
    job_addr = scrapy.Field(input_processor=MapCompose(remove_tags, handle_jobaddr))
    tags = scrapy.Field(input_processor=Join(","))
    company_url = scrapy.Field()
    company_name = scrapy.Field()
    degree_need = scrapy.Field(input_processor=MapCompose(rm_slash))
    crawl_time = scrapy.Field()
    salary = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                insert into lagou_job(title, url ,url_object_id, salary, job_city, work_years, degree_need, job_type, 
                tags, publish_time, job_advantage, job_desc, job_addr, company_name, company_url, crawl_time)values(%s,
                %s, %s , %s, %s, %s, %s , %s, %s, %s, %s , %s, %s, %s, %s , %s)ON DUPLICATE KEY UPDATE salary=VALUES(
                salary), job_desc=VALUES(job_desc), crawl_time=VALUES(crawl_time)
        
        """
        params = (
            self["title"], self["url"], self['url_object_id'], self['salary'], self['job_city'],
            self['work_years'], self['degree_need'], self['job_type'], self['tags'], self['publish_time'],
            self['job_advantage'], self['job_desc'], self['job_addr'], self['company_name'], self['company_url'],
            self['crawl_time'].strftime(SQL_DATETIME_FORMAT),
        )
        return insert_sql, params

    def save_to_es(self):
        lagou = LaGouType()
        lagou.title = self["title"]
        lagou.url = self["url"]
        lagou.meta.id = self["url_object_id"]
        lagou.job_city = self["job_city"]
        lagou.work_years = self["work_years"]
        lagou.job_type = self["job_type"]
        lagou.publish_time = self["publish_time"]
        lagou.job_advantage = self["job_advantage"]
        lagou.job_desc = self["job_desc"]
        lagou.job_addr = self["job_addr"]
        lagou.tags = self["tags"]
        lagou.company_url = self["company_url"]
        lagou.company_name = self["company_name"]
        lagou.degree_need = self["degree_need"]
        lagou.crawl_time = self["crawl_time"].strftime(SQL_DATETIME_FORMAT)
        lagou.salary = self["salary"]
        lagou.suggest = gen_suggests(LaGouType._doc_type.index, (
            (lagou.title, 10), (lagou.job_advantage, 6),
            (lagou.job_desc, 8), (lagou.company_name, 7)))
        lagou.save()
        return


def get_topics(value):
    return value.split(',')


def get_comment_num(value):
    match = re.match('(\d+)\s.*', value)
    if match:
        return int(match.group(1))
    else:
        return 0


def get_int_value(value):
    return int(value)


def get_answer_count(value):
    return int(value[0])


def get_watch_user_num(value):
    return int(value[0])


def get_click_num(value):
    return int(value[1])

def rm_html_tags(value):
    dr = re.compile(r'<[^>]+>', re.S)
    content = dr.sub('', value)
    match = re.match('(.*?)($|显示全部$)', content)
    if match:
        return match.group(1)
    else:
        return "什么内容也没有"


class ZhihuQuestionItem(scrapy.Item):
    # 知乎问题item
    question_id = scrapy.Field(input_processor=MapCompose(get_int_value), output_processor=TakeFirst())
    topics = scrapy.Field(output_processor=Join(','))
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    content = scrapy.Field(input_processor=MapCompose(rm_html_tags), output_processor=TakeFirst())
    answer_num = scrapy.Field(input_prosessor=MapCompose(get_answer_count))
    comment_num = scrapy.Field(input_processor=MapCompose(get_comment_num), output_processor=TakeFirst())
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field(output_processor=TakeFirst())

    def get_insert_sql(self):
        insert_sql = """
                insert into zhihu_question(question_id, topics, url, title, content, answer_num, comment_num, 
                watch_user_num, click_num, crawl_time)values(%s,
                %s, %s , %s, %s, %s, %s , %s, %s, %s) ON DUPLICATE KEY UPDATE content=VALUES(content), 
                comment_num=VALUES(comment_num), answer_num=VALUES(answer_num),
                watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)

        """
        try:
            self['answer_num'] = int(self['answer_num'][0])
        except Exception:
            self["answer_num"] = 0
        try:
            self['watch_user_num'] = int(self['watch_user_num'][0])
        except Exception:
            self['watch_user_num'] = 0
        try:
            self['click_num'] = int(self['click_num'][1])
        except Exception:
            self['click_num'] = 0

        params = (
            self['question_id'], self["topics"], self['url'], self['title'], self['content'],
            self['answer_num'], self['comment_num'], self['watch_user_num'], self['click_num'],  self['crawl_time']
        )
        return insert_sql, params

    def save_to_es(self):
        zhihu = ZhihuQuestionType()
        zhihu.meta.id = self["question_id"]
        zhihu.topics = self["topics"]
        zhihu.url = self["url"]
        zhihu.title = self["title"]
        try:
            if self["content"]:
                zhihu.content = self["content"]
        except Exception:
                zhihu.content = "什么内容也没有哦!"
        try:
            zhihu.answer_num = int(self["answer_num"][0])
        except Exception:
            zhihu.answer_num = 0
        zhihu.comment_num = self["comment_num"]
        try:
            zhihu.watch_user_num = int(self["watch_user_num"][0])
        except Exception:
            zhihu.watch_user_num = 0
        try:
            zhihu.click_num = int(self["click_num"][1])
        except Exception:
            zhihu.click_num = 0
        zhihu.crawl_time = self["crawl_time"]
        # article.suggest = gen_suggest(ArticleType._doc_type.index, ((article.title, 10), (article.tags, 7)))
        zhihu.suggest = gen_suggests(ZhihuQuestionType._doc_type.index, ((zhihu.title, 10), (zhihu.content, 9), (
                                    zhihu.topics, 7)))
        zhihu.save()
        return


class ZhihuAnswerItem(scrapy.Item):
    answer_id = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comment_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()
    # crawl_update_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                insert into zhihu_answer(answer_id, url ,question_id, author_id, content, praise_num, comment_num, 
                 update_time, crawl_time, create_time)values(%s, %s, %s , %s, %s, %s, %s , %s, %s, %s) ON DUPLICATE KEY
                 UPDATE content=VALUES(content), comment_num=VALUES(comment_num), praise_num=VALUES(praise_num), 
                 update_time=VALUES(update_time)
        """
        content = rm_html_tags(self['content'])
        type(content)
        params = (
            self["answer_id"], self["url"], self['question_id'], self['author_id'], content,
            self['praise_num'], self['comment_num'], self['update_time'], self['crawl_time'],
            self['create_time']
        )
        return insert_sql, params

    def save_to_es(self):
        zhihu = ZhihuAnswerType()
        zhihu.meta.id= self["answer_id"]
        zhihu.question_id = self["question_id"]
        zhihu.author_id = self["author_id"]
        zhihu.url = self["url"]
        zhihu.content = remove_tags(self["content"])
        zhihu.prise_num = self["praise_num"]
        zhihu.comment_num = self["comment_num"]
        zhihu.create_time= self["create_time"]
        zhihu.update_time = self["update_time"]
        zhihu.crawl_time = self["crawl_time"]
        # article.suggest = gen_suggest(ArticleType._doc_type.index, ((article.title, 10), (article.tags, 7)))
        zhihu.suggest = gen_suggests(ZhihuAnswerType._doc_type.index, ((zhihu.content, 10), ))
        zhihu.save()
        return



