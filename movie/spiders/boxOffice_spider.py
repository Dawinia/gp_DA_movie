import scrapy
import logging
from scrapy.loader import ItemLoader
from movie.items import BoxOfficeItem
import datetime
import json

logging.basicConfig(filename="boxOffice_spider.log", level=logging.WARNING,
                    format='%(asctime)s -  %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger('boxOfficeLogger')


def get_year_rate(date, rate):
    """ return the record year and corresponding rate as the primary key
        like 2016-01-01#1
    """
    return str(date) + f'#{rate}'


class BoxOfficeSpider(scrapy.Spider):
    def parse(self, response):
        pass

    name = "boxOffice"

    start_urls = ['http://piaofang.maoyan.com/second-box?beginDate=20160101', ]

    def start_requests(self):
        urls = ['http://piaofang.maoyan.com/second-box?beginDate=20160101', ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_boxoffice)

    def parse_boxoffice(self, response):
        item_loader = ItemLoader(item=BoxOfficeItem(), response=response)
        text = json.loads(response.text)
        logger.info(f'ok')

        for i, movie_info in enumerate(text['data']['list']):
            item_loader.replace_value('movieID', movie_info['movieId'])
            item_loader.replace_value('movieName', movie_info['movieName'])
            item_loader.replace_value('seatRate', movie_info['avgSeatView'])
            item_loader.replace_value('boxInfo', movie_info['boxInfo'])
            item_loader.replace_value('boxRate', movie_info['boxRate'])
            item_loader.replace_value('releaseInfo', movie_info['releaseInfo'])
            item_loader.replace_value('showInfo', movie_info['showInfo'])
            item_loader.replace_value('showRate', movie_info['showRate'])
            item_loader.replace_value('splitBoxInfo', movie_info['splitBoxInfo'])
            item_loader.replace_value('splitSumBoxInfo', movie_info['splitSumBoxInfo'])
            item_loader.replace_value('sumBoxInfo', movie_info['sumBoxInfo'])
            item_loader.replace_value('showView', movie_info['avgShowView'])
            item_loader.replace_value('crawlDate', datetime.date.today())
            item_loader.replace_value('yearRate', get_year_rate(datetime.date.today(), i + 1))
            logger.warning(f"get {i + 1} movie info, named {movie_info['movieName']}.")
            yield item_loader.load_item()

    def error_handler(self, failure):
        if failure.check():
            pass
