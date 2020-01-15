# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader import processors


def remove_unit(box: list):
    """ remove the unit
        if is billion then multiply as 10000
        final unit is 万
    """
    multi = 1
    box = box[0]
    if box.endswith('亿') or box.endswith('万'):
        if box.endswith('亿'):
            multi = 10000
        box = float(box[:-1]) * multi
        box = round(box, 2)
    return str(box)


class BoxOfficeItem(scrapy.Item):
    """ the filed of the BoxOffice """
    # define the fields for your item here like:
    # name = scrapy.Field()
    movieID = scrapy.Field()  # 电影ID,
    movieName = scrapy.Field()  # 电影名称,
    seatRate = scrapy.Field()  # 上座率,
    boxInfo = scrapy.Field(input_processor=remove_unit)  # 综合票房,
    boxRate = scrapy.Field()  # 票房占比,
    releaseInfo = scrapy.Field()  # 上映时间,
    showInfo = scrapy.Field()  # 排片场次,
    showRate = scrapy.Field()  # 排片占比,
    splitBoxInfo = scrapy.Field(input_processor=remove_unit)  # 分账票房,
    splitSumBoxInfo = scrapy.Field(input_processor=remove_unit)  # 总分账票房,
    sumBoxInfo = scrapy.Field(input_processor=remove_unit)  # 总综合票房,
    showView = scrapy.Field()  # 场均人次,
    crawlDate = scrapy.Field()  # 爬取日期
    yearRate = scrapy.Field()


class MovieItemLoader(ItemLoader):
    default_output_processor = processors.TakeFirst()
