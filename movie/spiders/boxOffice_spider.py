import scrapy
import logging
from scrapy.loader import ItemLoader
from movie.items import MovieItem
import json

logger = logging.getLogger('boxOfficeLogger')


class BoxOfficeSpider(scrapy.Spider):
    name = "boxOffice"

    def start_requests(self):
        start_urls = ['http://piaofang.maoyan.com/second-box?beginDate=20200111', ]

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item_loader = ItemLoader(item=MovieItem(), response=response)
        # text = response.xpath('//p/text()').get()
        # logger.info(f'parse page {response.text}')
        result = json.loads(response.text)
        logger.info(f'ok')

        # TODO: extract the data and parse it to item_loader
        # return item_loader.load_item()
        return result
