# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import create_engine


class MoviePipeline(object):
    def process_item(self, item, spider):
        engine = create_engine("mysql+pymysql://root:@ROOT_root_123/blog")
        return item
