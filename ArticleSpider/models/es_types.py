# coding=utf-8
__author__ = "alvin"
__date__ = "2018/4/26 16:17"
from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, Completion, Keyword, Text, Integer
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer


# 连接到服务器
connections.create_connection(hosts=["localhost"])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class ArticleType(DocType):
    suggest = Completion(analyzer=ik_analyzer)
    title = Text(analyzer='ik_max_word')  # text类型会分词解析
    create_date = Date()
    url = Keyword()  # 不进行分词解析，只进行全量保存
    url_object_id = Keyword()
    front_image_url = Keyword()
    front_image_path = Keyword()
    praise_num = Integer()
    comment_num = Integer()
    share_num = Integer()
    fav_num = Integer()
    tags = Text(analyzer='ik_max_word')
    content = Text(analyzer='ik_max_word')

    class Meta:
        index = "jobbole"
        doc_type = "article"


class ZhihuQuestionType(DocType):
    suggest = Completion(analyzer=ik_analyzer)
    question_id = Keyword()
    topics = Text(analyzer='ik_max_word')
    url = Keyword()
    title = Text(analyzer='ik_max_word')
    content = Text(analyzer='ik_max_word')
    answer_num = Integer()
    comment_num = Integer()
    watch_user_num = Integer()
    click_num = Integer()
    crawl_time = Date()

    class Meta:
        index = "zhihu"
        doc_type = "question"


class ZhihuAnswerType(DocType):
    suggest = Completion(analyzer=ik_analyzer)
    answer_id = Keyword()
    question_id = Keyword()
    author_id = Keyword()
    url = Keyword()
    content = Text(analyzer='ik_max_word')
    praise_num = Integer()
    comment_num = Integer()
    create_time = Date()
    update_time = Date()
    crawl_time = Date()

    class Meta:
        index = "zhihu"
        doc_type = "answer"


class LaGouType(DocType):
    suggest = Completion(analyzer=ik_analyzer)
    title = Text(analyzer='ik_max_word')
    url = Keyword()
    url_object_id = Keyword()
    job_city = Keyword()
    work_years = Keyword()
    job_type = Keyword()
    publish_time = Keyword()
    job_advantage = Text(analyzer='ik_max_word')
    job_desc = Text(analyzer='ik_max_word')
    job_addr = Keyword()
    tags = Text(analyzer='ik_max_word')
    company_url = Keyword()
    company_name = Text(analyzer='ik_max_word')
    degree_need = Keyword()
    crawl_time = Date()
    salary = Keyword()

    class Meta:
        index = "lagou"
        doc_type = "job"


if __name__ == '__main__':
    # ArticleType.init()
    ZhihuQuestionType.init()
    ZhihuAnswerType.init()
    # LaGouType.init()