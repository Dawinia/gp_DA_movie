# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from movie.dao import get_session
from movie.dao.databasetable import BoxOfficeTableTemplate
from movie.spiders.boxOffice_spider import logger


class BoxOfficePipeline(object):
    def __init__(self):
        self.id_seen = set()

    # @classmethod
    # def from_crawler(cls, crawler):
    #     pass
    #
    # def open_spider(self):
    #     pass
    #
    # def close_spider(self, spider):
    #     pass

    def process_item(self, item, spider):
        # if item['movie_id'] in self.id_seen:
        #     raise DropItem(f"Duplicate item found :{item}")
        # else:
        #     self.id_seen.add(item['movie_id'])
        return item


class MySQLPipeline(object):
    def __init__(self):
        self.id_seen = set()
        logger.warning(f"pipeline init")
        self.session = get_session()

    # @classmethod
    # def from_crawler(cls, crawler):
    #     pass
    #
    # def open_spider(self):
    #     pass

    def close_spider(self, spider):  # 关闭爬虫时
        self.session.close()

    def process_item(self, item, spider):
        self.session.add(BoxOfficeTableTemplate(**item))
        logger.warning(f"insert database finished")
        self.session.commit()
