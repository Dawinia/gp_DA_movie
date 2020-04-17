# # encoding: utf-8
# """
# @author: dawinia
# @time: 2020/4/16 上午12:28
# @file: origin.py
# @desc:
# """
# from json import JSONDecodeError
# from urllib.parse import urlencode
#
# import scrapy
# import logging
# from scrapy.loader import ItemLoader
# from movie.items import BoxOfficeItem, MovieCommentItem
# import datetime
# import time
# import json
# import re
# import requests
# from fake_useragent import UserAgent
# from scrapy.utils.project import get_project_settings
# import random
#
#
# settings = get_project_settings()
#
# logging.basicConfig(
#     filename=settings['BOXOFFICE_LOG_FILE'],
#     level=logging.WARNING,
#     format='%(asctime)s -  %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
# logger = logging.getLogger('boxOfficeLogger')
#
#
# def get_year_rate(year, rate):
#     """
#     return the record year and corresponding rate as the primary key
#     :param year: like 20160101
#     :param rate: like 1
#     :return: like 2016-01-01#1
#     """
#     return str(year) + f'#{rate}'
#
#
# def is_legal_date(date: str) -> bool:
#     """
#     if the str is a legal date
#     :param date: the str about date
#     :return: True if the str is legal
#     """
#     try:
#         time.strptime(date, "%Y%m%d")
#         return True
#     except BaseException:
#         return False
#
#
# def get_random_headers():
#     return {'User-Agent': str(UserAgent().random)}
#
#
# class MovieSpider(scrapy.Spider):
#     name = "movie"
#     custom_settings = {
#         'SET_TEST': 'custom boxOffice setting',
#     }
#
#     def __init__(self, *args, **kwargs):
#         super(MovieSpider, self).__init__(*args, **kwargs)
#         self.proxies = settings.get('PROXY_URL')
#         self.headers = get_random_headers()
#
#     # start_urls = ['http://piaofang.maoyan.com/second-box?beginDate=20160101', ]
#     search_base_url = "https://movie.douban.com/j/subject_suggest?q="
#     comment_base_url = "https://movie.douban.com/subject/{}/comments"
#
#     def start_requests(self):
#         data = {'beginDate': 20160101}
#         base_url = 'http://piaofang.maoyan.com/second-box?'
#         logger.error(f"boxOffice start request for url = {base_url}")
#         for date in range(self.settings.get('BEGIN_DATE'), self.settings.get('END_DATE') + 1):
#             if not is_legal_date(str(date)):
#                 continue
#             data['beginDate'] = date
#             params = urlencode(data)
#             url = base_url + params
#             yield scrapy.Request(url=url, callback=self.parse_box_info)
#
#     def parse(self, response):
#         pass
#
#     def parse_box_info(self, response):
#         """
#         获取每日电影票房信息
#         :param response:
#         :return:
#         """
#         logger.error(f"now crawl url : {response.url}")
#         item_loader = ItemLoader(item=BoxOfficeItem(), response=response)
#         text = json.loads(response.text)
#
#         query_date = text.get('data').get('queryDate')
#         for i, movie_info in enumerate(text.get('data').get('list')):
#             field_map = {
#                 'movieID': 'movieId',
#                 'movieName': 'movieName',
#                 'seatRate': 'avgSeatView',
#                 'boxInfo': 'boxInfo',
#                 'boxRate': 'boxRate',
#                 'releaseInfo': 'releaseInfo',
#                 'showInfo': 'showInfo',
#                 'showRate': 'showRate',
#                 'splitBoxInfo': 'splitBoxInfo',
#                 'splitSumBoxInfo': 'splitSumBoxInfo',
#                 'sumBoxInfo': 'sumBoxInfo',
#                 'showView': 'avgShowView'
#             }
#             for field, json_attr in field_map.items():
#                 item_loader.replace_value(field, movie_info.get(json_attr))
#             item_loader.replace_value('crawlDate', datetime.date.today())
#             item_loader.replace_value('yearRate', get_year_rate(query_date, i + 1))
#             logger.warning(f"get {i + 1} movie info, named {movie_info.get('movieName')}.")
#             # logger.error(f"boxOffice spider put {movie_info.get('movieName')} into queue")
#             yield item_loader.load_item()
#
#             # 根据电影名称从豆瓣获取电影详情页链接
#             movie_name = movie_info.get('movieName')
#             movie_id = movie_info.get('movieId')
#             search_url = self.search_base_url + movie_name
#             yield scrapy.Request(url=search_url, callback=self.parse_movie_info_url,
#                                  cb_kwargs=dict(movie_name=movie_name, movie_year=query_date, tpp_id=movie_id))
#
#         logger.error(f"boxOffice start parse")
#
#     def parse_movie_info_url(self, response, movie_name, movie_year, tpp_id):
#         """
#         获取电影详情页链接，并转入 parse_movie_info 处理
#         :param tpp_id: 淘票票 ID
#         :param movie_year: 爬取日期信息
#         :param movie_name: 爬取电影名称
#         :param response:
#         :return:
#         """
#         logger.error(f"movie_name = {movie_name} and movie_year = {movie_year} and tpp_id = {tpp_id}")
#         if len(movie_name) == 0 or len(movie_year) == 0:
#             logger.error(f"kwargs not assign")
#             return
#         text = json.loads(response.text)
#         logger.error(f"len of text is {len(text)}")
#         if len(text) == 0:
#             logger.error(f"not response scraped")
#             return
#         movie_url = ""
#         for detail in text:
#             if len(detail.get('episode')):
#                 continue
#             if detail.get('title') == movie_name and detail.get('year') == movie_year[:4]:
#                 movie_url = detail.get('url')
#         if len(movie_url) == 0:
#             logger.error(f"url wrong that url = {movie_url}")
#             return
#         logger.error(f"get movie info url = {movie_url}")
#         yield scrapy.Request(url=movie_url, callback=self.parse_movie_info, cb_kwargs=dict(tpp_id=tpp_id))
#
#     def parse_movie_info(self, response, tpp_id):
#         item_loader = ItemLoader(item=MovieCommentItem, response=response)
#         data = response.xpath("//script[@type='application/ld+json']/text()")
#         text = json.loads(data)
#
#         item_loader.replace_value('movieName', text.get('name'))
#         item_loader.replace_value('dbMovieID', text.get('url')[9: -1])
#         item_loader.replace_value('tppMovieID', tpp_id)
#
#         def get_name_list(parent):
#             return [child.get('name').split(' ')[0] for child in text.get(parent)]
#
#         item_loader.replace_value('directors', get_name_list('directors'))
#         item_loader.replace_value('writers', get_name_list('writers'))
#         item_loader.replace_value('actors', get_name_list('actors'))
#
#         item_loader.replace_value('genre', text.get('genre'))
#
#         info = response.xpath('//*[@id="info"]').get()
#         pattern = '<span class="pl">制片国家/地区:</span>(.*?)<br/>'
#         item_loader.replace_value('area', re.findall(pattern, info))
#         item_loader.replace_value('duration', text.get('duration'))
#         item_loader.replace_value('publishedDate', text.get('datePublished'))
#         item_loader.replace_value('rateCount', text.get('aggregateRating').get('ratingCount'))
#         item_loader.replace_value('doubanRate', text.get('aggregateRating').get('ratingValue'))
#
#         yield item_loader.load_item()
#
#         # yield scrapy.Request()
#
#
#     def parse_movie_comment(self):
#         pass
#
#     def error_handler(self, failure):
#         if failure.check():
#             pass
#
#
# """class MovieCommentSpider(scrapy.Spider):
#     name = "movieComment"
#     custom_settings = {
#         'SET_TEST': 'custom movie comment setting',
#     }
#
#     def __init__(self, *args, **kwargs):
#         super(MovieCommentSpider, self).__init__(*args, **kwargs)
#         self.queue: Queue = kwargs.get('queue')
#
#     def start_requests(self):
#         base_url = 'https://www.baidu.com'
#         logger.error(f"movie comment start request url = {base_url}")
#         yield scrapy.Request(url=base_url, callback=self.parse)
#
#     def parse(self, response):
#         logger.error(f"movie comment start parse")
#         movie_name = self.queue.get()
#         logger.error(f"boxOffice spider get {movie_name} from queue")
# """
