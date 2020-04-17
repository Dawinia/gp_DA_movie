# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader import processors
from scrapy.loader.processors import Join, MapCompose


def get_minute(time: str):
    """
    根据给定时间表达式（固定格式）返回分钟数
    :param time: 时间表达式，格式为 PTaHbM， a为小时数，b为分钟数
    :return: 返回分钟数
    """
    hour_pos = time.find('H')
    minute_pos = time.find('M')
    return time[hour_pos - 1: hour_pos] * 60 + time[hour_pos + 1: minute_pos]


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


class MovieCommentItem(scrapy.Item):
    pass


class MovieInfoItem(scrapy.Item):
    """ the filed of the movie info """
    movieName = scrapy.Field()  # 电影名称
    dbMovieID = scrapy.Field()  # 豆瓣电影ID
    tppMovieID = scrapy.Field()  # 淘票票电影ID
    directors = scrapy.Field(output_processor=Join('/'))  # 导演
    writers = scrapy.Field(output_processor=Join('/'))  # 编剧
    actors = scrapy.Field(output_processor=Join('/'))  # 演员表
    genre = scrapy.Field(output_processor=Join('/'))  # 电影类型列表
    area = scrapy.Field(output_processor=Join('/'))  # 制片国家/地区
    duration = scrapy.Field(input_processor=MapCompose(get_minute))  # 电影时长
    publishedDate = scrapy.Field()  # 上映日期
    rateCount = scrapy.Field()  # 评分人数
    doubanRate = scrapy.Field()  # 豆瓣评分


class MovieItemLoader(ItemLoader):
    default_output_processor = processors.TakeFirst()
