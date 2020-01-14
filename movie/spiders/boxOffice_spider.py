import scrapy
import logging
from twisted.internet import reactor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerRunner
from movie.items import BoxOfficeItem
import datetime
from scrapy.utils.log import configure_logging
import json

logging.basicConfig(filename="boxOffice_spider.log")
logger = logging.getLogger('boxOfficeLogger')

# TODO: add logger and test


class BoxOfficeSpider(scrapy.Spider):
    name = "boxOffice"

    start_urls = ['http://piaofang.maoyan.com/second-box?beginDate=20160101', ]

    def parse(self, response):
        item_loader = ItemLoader(item=BoxOfficeItem(), response=response)
        # text = response.xpath('//p/text()').get()
        # logger.info(f'parse page {response.text}')
        text = json.loads(response.text)
        logger.info(f'ok')

        for i, movie_info in enumerate(text['data']['list']):
            item_loader.add_value('movie_id', movie_info['movieID'])
            item_loader.add_value('movie_name', movie_info['movieName'])
            item_loader.add_value('movie_seatRate', movie_info['avgSeatView'])
            item_loader.add_value('movie_boxInfo', movie_info['boxInfo'])
            item_loader.add_value('movie_boxRate', movie_info['boxRate'])
            item_loader.add_value('movie_releaseInfo', movie_info['releaseInfo'])
            item_loader.add_value('movie_showInfo', movie_info['showInfo'])
            item_loader.add_value('movie_showRate', movie_info['showRate'])
            item_loader.add_value('movie_splitBoxInfo', movie_info['splitBoxInfo'])
            item_loader.add_value('movie_splitSumBoxInfo', movie_info['splitSumBoxInfo'])
            item_loader.add_value('movie_sumBoxInfo', movie_info['sumBoxInfo'])
            item_loader.add_value('movie_showView', movie_info['avgShowView'])
            item_loader.add_value('crawl_date', datetime.date.today())
            yield item_loader.load_item()

        # TODO: extract the data and parse it to item_loader
        # return item_loader.load_item()

    def error_handler(self, failure):
        if failure.check():
            pass
