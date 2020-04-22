# encoding: utf-8
"""
@author: dawinia
@time: 2020/4/21 上午1:13
@file: BaseCrawler.py
@desc: 
"""
import requests
from lxml import etree
from ProxyPool.settings import HEADER
from retrying import retry


class BaseCrawler:
    urls = []

    def __init__(self):
        self.headers = HEADER

    @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None)
    def fetch(self, url, **kwargs):
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return etree.HTML(response.text)
        except requests.ConnectionError:
            return

    def crawl(self):
        """
        get proxy from xicidaili
        :return:
        """
        for url in self.urls:
            html = self.fetch(url)
            for proxy in self.parse(html):
                yield proxy
