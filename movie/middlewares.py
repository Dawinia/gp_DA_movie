# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import requests

from ProxyPool.scheme.Proxy import Proxy
from logger import Logger
from movie.dao import RedisHelper
from hashlib import md5
from fake_useragent import UserAgent
import random

logger = Logger('boxOfficeLogger').getlog()


class MovieSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        pass
        # spider.logger.info('Spider opened: %s' % spider.module_name)


class MovieDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        pass
        # spider.logger.info('Spider opened: %s' % spider.module_name)


class CookiesMiddleware(object):
    """ 随机设置Cookies """

    def __init__(self):
        pass

    def process_request(self):
        pass

    def process_response(self):
        pass

    def from_crawler(self):
        pass


class DuplicateMiddleware(object):
    def __init__(self, redis_helper: RedisHelper, key):
        logger.info(f"start to use judge duplicate url")
        self.conn = redis_helper.get_conn()
        self.key = key

    def process_request(self, request, spider):
        """ 使用 md5 对 URL 进行加密，并加入 set， 若 set 中已存在，则不继续该请求 """
        md5_obj = md5()
        md5_obj.update(request.url.encode(encoding='utf-8'))
        new_url = md5_obj.hexdigest()
        if self.conn.sadd(self.key, new_url) == 0:
            logger.error(f"{request.url} has been crawled, drop it")
            # raise IgnoreRequest(f"{request.url} has been crawled")
        return None

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            RedisHelper(settings.get('REDIS_HOST'), settings.get('REDIS_PORT'), settings.get('REDIS_PASSWORD')),
            settings.get('URL_SEEN')
        )


class UserAgentMiddleware(object):
    """ 随机更换 User-Agent """

    def __init__(self, crawler):
        super(UserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UserAgent_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault('User-Agent', get_ua())


class ProxyMiddleware(object):
    """ 随机获取代理 """

    def __init__(self, proxy_url: list):
        super(ProxyMiddleware, self).__init__()
        self.proxy_url = proxy_url

    def get_random_proxy(self):
        try:
            # response = requests.get(self.proxy_url)
            # if response.status_code == 200:
            #    proxy = response.text
            proxy = random.choice(self.proxy_url)
            return proxy
        except requests.ConnectionError:
            return None

    def process_request(self, request, spider):
        # if request.meta.get('retry_times'):
        proxy = requests.get('http://localhost:21642/random').text.strip()
        proxy = proxy[1:].split(':')
        proxy = 'http://' + Proxy(proxy[0][1:-1], int(proxy[1])).string()
        print(proxy)
        if proxy:
            logger.info('使用代理 ' + proxy)
            request.meta['proxy'] = proxy

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )


class RefererMiddleware(object):
    def process_request(self, request, spider):
        # if request.meta.get('retry_times'):
        referer = "https://movie.douban.com/"
        if referer:
            request.headers["referer"] = referer
