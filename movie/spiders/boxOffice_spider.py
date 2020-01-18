from urllib.parse import urlencode

import scrapy
import logging
from scrapy.loader import ItemLoader
from movie.items import BoxOfficeItem
import datetime
import time
import json
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

logging.basicConfig(filename=settings['BOXOFFICE_LOG_FILE'], level=logging.WARNING,
                    format='%(asctime)s -  %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger('boxOfficeLogger')


def get_year_rate(year, rate):
    """
    return the record year and corresponding rate as the primary key
    :param year: like 20160101
    :param rate: like 1
    :return: like 2016-01-01#1
    """
    return str(year) + f'#{rate}'


def is_legal_date(date: str) -> bool:
    """
    if the str is a legal date
    :param date: the str about date
    :return: True if the str is legal
    """
    try:
        time.strptime(date, "%Y%m%d")
        return True
    except :
        return False


class BoxOfficeSpider(scrapy.Spider):
    def parse(self, response):
        pass

    name = "boxOffice"

    # start_urls = ['http://piaofang.maoyan.com/second-box?beginDate=20160101', ]

    def start_requests(self):
        data = {'beginDate': 20160101}
        base_url = 'http://piaofang.maoyan.com/second-box?'
        for date in range(20160101, self.settings.get('END_DATE') + 1):
            if not is_legal_date(str(date)):
                continue
            data['beginDate'] = date
            params = urlencode(data)
            url = base_url + params
            yield scrapy.Request(url=url, callback=self.parse_boxoffice)

    def parse_boxoffice(self, response):
        # logger.error(f"now crawl url : {response.url}")
        item_loader = ItemLoader(item=BoxOfficeItem(), response=response)
        text = json.loads(response.text)
        logger.info(f'ok')

        for i, movie_info in enumerate(text.get('data').get('list')):
            item_loader.replace_value('movieID', movie_info.get('movieId'))
            item_loader.replace_value('movieName', movie_info.get('movieName'))
            item_loader.replace_value('seatRate', movie_info.get('avgSeatView'))
            item_loader.replace_value('boxInfo', movie_info.get('boxInfo'))
            item_loader.replace_value('boxRate', movie_info.get('boxRate'))
            item_loader.replace_value('releaseInfo', movie_info.get('releaseInfo'))
            item_loader.replace_value('showInfo', movie_info.get('showInfo'))
            item_loader.replace_value('showRate', movie_info.get('showRate'))
            item_loader.replace_value('splitBoxInfo', movie_info.get('splitBoxInfo'))
            item_loader.replace_value('splitSumBoxInfo', movie_info.get('splitSumBoxInfo'))
            item_loader.replace_value('sumBoxInfo', movie_info.get('sumBoxInfo'))
            item_loader.replace_value('showView', movie_info.get('avgShowView'))
            item_loader.replace_value('crawlDate', datetime.date.today())
            item_loader.replace_value('yearRate', get_year_rate(datetime.date.today(), i + 1))
            logger.warning(f"get {i + 1} movie info, named {movie_info.get('movieName')}.")
            yield item_loader.load_item()

    def error_handler(self, failure):
        if failure.check():
            pass
