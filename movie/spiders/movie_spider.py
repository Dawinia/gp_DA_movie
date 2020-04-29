from json import JSONDecodeError
from urllib.parse import urlencode

import scrapy
import logging
from scrapy.loader import ItemLoader
from movie.items import BoxOfficeItem, MovieCommentItem, MovieInfoItem, PersonInfoItem
import datetime
import time
import json
import re
import requests
from fake_useragent import UserAgent
from scrapy.utils.project import get_project_settings
import random

settings = get_project_settings()

logging.basicConfig(
    filename=settings['BOXOFFICE_LOG_FILE'],
    level=logging.INFO,
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
    except BaseException:
        return False


def get_random_headers():
    return {'User-Agent': str(UserAgent().random)}


class MovieSpider(scrapy.Spider):
    name = "movie"
    custom_settings = {
        'SET_TEST': 'custom boxOffice setting',
    }

    def __init__(self, *args, **kwargs):
        super(MovieSpider, self).__init__(*args, **kwargs)
        self.proxies = settings.get('PROXY_URL')
        self.headers = get_random_headers()
        self.cookies = {
            'll': '"108288"',
            'bid': 'rQ_4eLifMgk',
            '__yadk_uid': 'haNwNJD1SOvT7N2GUhsgUDGtkZEUq7g7',
            '_vwo_uuid_v2': 'D44C636A7D0473EA64ED8C40CC931ADA5|6967f27cc44f600b5a095023c436bfec',
            'trc_cookie_storage': 'taboola%2520global%253Auser-id%3D3887b9e3-3ebe-4d7d-9401-e4ca4225e9fe-tuct404d423',
            'douban-fav-remind': '1',
            '__utmv': '30149280.15543', 'viewed': '"23008813"',
            'gr_user_id': '996ce25d-8d0b-408b-b8fd-80b4e71b20eb',
            '__utmz': '30149280.1585738212.13.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
            '__utma': '30149280.718043312.1579062981.1586961198.1587105742.15',
            '__utmc': '30149280',
            '__utmt': '1',
            'ap_v': '0,6.0',
            '__utmb': '30149280.4.10.1587105742',
            '_pk_ref.100001.4cf6': '%5B%22%22%2C%22%22%2C1587105809%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D',
            '_pk_ses.100001.4cf6': '*',
            '__utma': '223695111.2040974979.1579062981.1580218194.1587105809.13',
            '__utmb': '223695111.0.10.1587105809',
            '__utmc': '223695111',
            '__utmz': '223695111.1587105809.13.10.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
            'dbcl2': '"155437982:twOTXHGvmUg"',
            'ck': '-c5o',
            '_pk_id.100001.4cf6': '20e2b7b939cde70d.1579062981.13.1587105873.1580218193.',
            'push_noty_num': '0', 'push_doumail_num': '0'}

    # start_urls = ['http://piaofang.maoyan.com/second-box?beginDate=20160101', ]
    search_base_url = "https://movie.douban.com/j/subject_suggest?q="
    comment_base_url = "https://movie.douban.com/subject/{}/comments"

    def start_requests(self):
        data = {'showDate': 20160101}
        base_url = 'http://piaofang.maoyan.com/dashboard-ajax/movie?'
        logger.error(f"boxOffice start request for url = {base_url}")
        for date in range(self.settings.get('BEGIN_DATE'), self.settings.get('END_DATE') + 1):
            if not is_legal_date(str(date)):
                continue
            data['showDate'] = date
            params = urlencode(data)
            url = base_url + params
            yield scrapy.Request(url=url, callback=self.parse_box_info, dont_filter=True)

    def parse(self, response):
        pass

    def parse_box_info(self, response):
        """
        获取每日电影票房信息
        :param response:
        :return:
        """
        time.sleep(random.uniform(0, 1))
        logger.error(f"now crawl url : {response.url}")
        item_loader = ItemLoader(item=BoxOfficeItem(), response=response)
        text = json.loads(response.text)

        query_date = text.get('calendar', []).get('selectDate', "")
        for i, movie_info in enumerate(text.get('movieList', []).get('list', [])):
            if i == 30:
                break
            field_map = {
                'seatRate': 'avgSeatView',
                'boxRate': 'boxRate',
                'showRate': 'showCountRate',
                'splitSumBoxInfo': 'sumSplitBoxDesc',
                'sumBoxInfo': 'sumBoxDesc',
                'showView': 'avgShowView'
            }
            movie_name = movie_info.get('movieInfo', []).get('movieName')
            movie_id = movie_info.get('movieInfo', []).get('movieId')
            for field, json_attr in field_map.items():
                item_loader.replace_value(field, movie_info.get(json_attr, ''))
            item_loader.replace_value('movieID', movie_id)
            item_loader.replace_value('movieName', movie_name)
            item_loader.replace_value('releaseInfo', movie_info.get('movieInfo', []).get('releaseInfo', ""))
            item_loader.replace_value('showInfo', movie_info.get('showCount', 0))
            item_loader.replace_value('boxInfo', movie_info.get('boxSplitUnit', []).get('num', ""))
            item_loader.replace_value('splitBoxInfo', movie_info.get('splitBoxSplitUnit', []).get('num', ""))
            item_loader.replace_value('crawlDate', query_date)
            item_loader.replace_value('yearRate', get_year_rate(query_date, i + 1))
            logger.warning(f"get {i + 1} movie info, named {movie_info.get('movieName', '')}.")
            # logger.error(f"boxOffice spider put {movie_info.get('movieName')} into queue")
            yield item_loader.load_item()

            # 根据电影名称从豆瓣获取电影详情页链接
            search_url = self.search_base_url + movie_name

            time.sleep(random.uniform(0, 1))

            yield scrapy.Request(url=search_url, cookies=self.cookies, callback=self.parse_movie_info_url,
                                 dont_filter=True,
                                 cb_kwargs=dict(movie_name=movie_name, movie_year=query_date, tpp_id=movie_id))

        logger.error(f"boxOffice start parse")

    def parse_movie_info_url(self, response, movie_name, movie_year, tpp_id):
        """
        获取电影详情页链接，并转入 parse_movie_info 处理
        :param tpp_id: 淘票票 ID
        :param movie_year: 爬取日期信息
        :param movie_name: 爬取电影名称
        :param response:
        :return:
        """
        logger.info(f"movie_name = {movie_name} and movie_year = {movie_year} and tpp_id = {tpp_id}")
        if len(movie_name) == 0 or len(movie_year) == 0:
            logger.error(f"kwargs not assign")
            return
        text = json.loads(response.text)
        logger.info(f"the url is {response.url}")
        logger.info(f"len of text is {len(text)}")
        if len(text) == 0:
            logger.error(f"not response scraped")
            return
        movie_url = ""
        for detail in text:
            if 'episode' in detail and len(detail.get('episode', [])):
                continue
            # if detail.get('title', '') == movie_name and detail.get('year', '') == movie_year[:4]:
            if detail.get('title', '') == movie_name:
                movie_url = detail.get('url', '')
        if len(movie_url) == 0:
            logger.error(f"url wrong that url = {movie_url}")
            return
        logger.error(f"get movie info url = {movie_url}")
        time.sleep(random.uniform(1, 2))
        movie_url = 'https://movie.douban.com/subject/34970135/?suggest=%E7%85%A7%E7%9B%B8%E5%B8%88'
        yield scrapy.Request(url=movie_url, cookies=self.cookies, callback=self.parse_movie_info, dont_filter=True,
                             cb_kwargs=dict(tpp_id=tpp_id))

    def parse_movie_info(self, response, tpp_id):
        logger.critical(f"crawled movie info of {response.url}")
        item_loader = ItemLoader(item=MovieInfoItem(), response=response)
        person_item_loader = ItemLoader(item=PersonInfoItem(), response=response)
        data = response.xpath("//script[@type='application/ld+json']/text()").extract()[0]
        logger.critical(f"type of data is {type(data)}")
        try:
            text = json.loads(data)
        except json.decoder.JSONDecodeError as de:
            logger.error(f"json decode error {de} in url = {response.url}")
        finally:
            text = json.loads(data)

        logger.error(f"len of movie info = {len(text)}")
        item_loader.replace_value('movieName', text.get('name', ''))
        item_loader.replace_value('movieName', text.get('name', ''))
        item_loader.replace_value('dbMovieID', text.get('url', '')[9: -1])
        item_loader.replace_value('tppMovieID', tpp_id)

        def get_name_list(parent):
            result = [child.get('name', '').split(' ')[0] for child in text.get(parent, [])][:10]
            return result if len(result) else [""]

        def get_person_info(parent):
            logger.info(f"start to crawl person")
            for detail in text.get(parent, []):
                person_item_loader.replace_value('name', detail.get('name', ''))
                person_item_loader.replace_value('url', detail.get('url', ''))
                person_item_loader.replace_value('identity', parent)
                yield person_item_loader.load_item()

        logger.critical(f"items = {get_name_list('actor')}")
        print(f"items = {get_name_list('actor')}")
        item_loader.replace_value('directors', get_name_list('director'))
        item_loader.replace_value('writers', get_name_list('author'))
        item_loader.replace_value('actors', get_name_list('actor'))

        item_loader.replace_value('genre', text.get('genre', ''))

        info = response.xpath('//*[@id="info"]').get()
        pattern = '<span class="pl">制片国家/地区:</span>(.*?)<br>'
        item_loader.replace_value('area', re.findall(pattern, info))
        item_loader.replace_value('duration', text.get('duration', ''))
        item_loader.replace_value('publishedDate', text.get('datePublished', ''))
        item_loader.replace_value('rateCount', text.get('aggregateRating', []).get('ratingCount', ''))
        item_loader.replace_value('doubanRate', text.get('aggregateRating', []).get('ratingValue', ''))

        yield item_loader.load_item()

        time.sleep(random.uniform(1, 2))

        get_person_info('director')
        get_person_info('author')
        get_person_info('actor')

        # yield scrapy.Request()

    def parse_movie_comment(self):
        pass

    def error_handler(self, failure):
        if failure.check():
            pass


"""class MovieCommentSpider(scrapy.Spider):
    name = "movieComment"
    custom_settings = {
        'SET_TEST': 'custom movie comment setting',
    }

    def __init__(self, *args, **kwargs):
        super(MovieCommentSpider, self).__init__(*args, **kwargs)
        self.queue: Queue = kwargs.get('queue')

    def start_requests(self):
        base_url = 'https://www.baidu.com'
        logger.error(f"movie comment start request url = {base_url}")
        yield scrapy.Request(url=base_url, callback=self.parse)

    def parse(self, response):
        logger.error(f"movie comment start parse")
        movie_name = self.queue.get()
        logger.error(f"boxOffice spider get {movie_name} from queue")
"""
