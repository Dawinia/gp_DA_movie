# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader import processors


class BoxOfficeItem(scrapy.Item):
    """ the filed of the BoxOffice """
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_id = scrapy.Field()                       # 电影ID,
    movie_name = scrapy.Field()                     # 电影名称,
    movie_seatRate = scrapy.Field()                 # 上座率,
    movie_boxInfo = scrapy.Field()                  # 综合票房,
    movie_boxRate = scrapy.Field()                  # 票房占比,
    movie_releaseInfo = scrapy.Field()              # 上映时间,
    movie_showInfo = scrapy.Field()                 # 排片场次,
    movie_showRate = scrapy.Field()                 # 排片占比,
    movie_splitBoxInfo = scrapy.Field()             # 分账票房,
    movie_splitSumBoxInfo = scrapy.Field()          # 总分账票房,
    movie_sumBoxInfo = scrapy.Field()               # 总综合票房,
    movie_showView = scrapy.Field()                 # 场均人次,
    crawl_date = scrapy.Field()                     # 爬取日期


class MovieItemLoader(ItemLoader):
    default_output_processor = processors.TakeFirst()
