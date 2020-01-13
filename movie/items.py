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
    movie_name = scrapy.Field()
    crawl_date = scrapy.Field()
    movie_duration = scrapy.Field()
    movie_boxOffice = scrapy.Field()
    movie_schedule = scrapy.Field()
    schedule_rate = scrapy.Field()
    average_per = scrapy.Field()


class MovieItemLoader(ItemLoader):
    default_output_processor = processors.TakeFirst()