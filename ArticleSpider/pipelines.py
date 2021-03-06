# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from MySQLdb.cursors import DictCursor
from w3lib.html import remove_tags

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 自定义json文件导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()

#
# class MysqlPipeline(object):
#     # 采用同步机制导入数据库
#     def __init__(self):
#         self.conn = MySQLdb.connect('127.0.0.1', 'root', '', 'article', charset='utf8', use_unicode=True)
#         self.cursor = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         insert_sql = 'insert into jobbole(title, url, create_date, fav_num) VALUES (%s, %s, %s, %s)'
#         self.cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_num"]))
#         self.conn.commit()


class MysqlTwistedPipeline(object):
    # 采用异步机制导入数据库
    def __init__(self, dbpool):
        self.dbpool = dbpool
    # 从配置中获取信息

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入编程异步执行
        # 第一个参数是我们定义的函数
        query = self.dbpool.runInteraction(self.do_insert, item)
        #错误处理
        query.addErrback(self.handle_error, item, spider)

    # 错误处理函数
    def handle_error(self, failure, item, spider):
          print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


class JsonExporterPipeline(object):
    # 调用scrapy提供的json_export到处json文件
    def __init__(self):
        self.file = open('articleexporter.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path
        return item


class ElasticSearchPipeline(object):
    # 将数据写入到es中
    def process_item(self, item, spider):
        # 将item转换为es的数据
        item.save_to_es()
        return item





