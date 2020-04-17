# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from movie.dao import MySQLHelper
from movie.dao.databasetable import BoxOfficeTableTemplate, MovieInfoTableTemplate, PersonTableTemplate
from movie.spiders.movie_spider import logger
from movie.items import BoxOfficeItem, MovieCommentItem, MovieInfoItem, PersonInfoItem


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
    def __init__(self, mysql_helper: MySQLHelper):
        self.session = mysql_helper.get_session()
        self.id_seen = set()
        logger.error(f"pipeline init")

    @classmethod
    def from_crawler(cls, crawler):
        logger.error(f"setting: {crawler.settings.get('SET_TEST')}")
        settings = crawler.settings
        return cls(MySQLHelper(settings['DATABASE_USER'], settings['DATABASE_PASSWORD'], settings['DATABASE_PORT'],
                               settings['DATABASE_NAME']))

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):  # 关闭爬虫时
        self.session.close()

    def process_item(self, item, spider):
        logger.critical(f"type of item is {type(item)}")
        if isinstance(item, BoxOfficeItem):
            self.session.add(BoxOfficeTableTemplate(**item))
        elif isinstance(item, MovieInfoItem):
            self.session.add(MovieInfoTableTemplate(**item))
        elif isinstance(item, PersonInfoItem):
            self.session.add(PersonTableTemplate(**item))
        # elif isinstance(item, MovieCommentItem):
        #     self.session.add(MovieCommentTableTemplate(**item))
        logger.warning(f"insert database finished")
        self.session.commit()
