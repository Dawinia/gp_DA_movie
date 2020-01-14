# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader import processors


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_name = scrapy.Field()                 # 电影名字
    crawl_date = scrapy.Field()                 # 爬取日期
    movie_duration = scrapy.Field()             # 上映日期
    movie_boxOffice = scrapy.Field()            # 电影票房
    box_Office_rate = scrapy.Field()            # 票房占比
    movie_schedule = scrapy.Field()             # 排片场次
    schedule_rate = scrapy.Field()              # 排片占比
    average_per = scrapy.Field()                # 场均人次


class MovieItemLoader(ItemLoader):
    default_output_processor = processors.TakeFirst()