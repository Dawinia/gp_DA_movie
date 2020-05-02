# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from movie.dao import MySQLHelper, RedisHelper
from movie.dao.databasetable import BoxOfficeTableTemplate, MovieInfoTableTemplate, PersonTableTemplate
from logger import Logger
from movie.items import BoxOfficeItem, MovieCommentItem, MovieInfoItem, PersonInfoItem
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import session

logger = Logger('boxOfficeLogger').getlog()


class BoxOfficePipeline(object):
    def __init__(self, redis_helper: RedisHelper):
        logger.error(f"start to use judge duplicate")
        self.conn = redis_helper.get_conn()

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            RedisHelper(settings.get('REDIS_HOST'), settings.get('REDIS_PORT'), settings.get('REDIS_PASSWORD'))
        )
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
        # key, value = 'default', 'default'
        if isinstance(item, BoxOfficeItem):
            key, value = 'boxOffice', item['yearRate'][0]
        elif isinstance(item, MovieInfoItem):
            key, value = 'movieInfo', item['dbMovieID'][0]
        elif isinstance(item, PersonInfoItem):
            key, value = 'personInfo', item['name'][0]
        else:
            key, value = 'default', 'default'

        if not self.conn.sadd(key, value):
            raise DropItem(f"Duplicate item found :{value}")
        else:
            logger.info(f"item is new")
            return item


class MySQLPipeline(object):
    def __init__(self, mysql_helper: MySQLHelper):
        self.session: session = mysql_helper.get_session()
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
        try:
            self.session.commit()
        except InvalidRequestError:
            logger.error(f"something wrong occur, session rollback")
            self.session.rollback()
