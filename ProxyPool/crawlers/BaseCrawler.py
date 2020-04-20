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


class BaseCrawler:
    urls = []

    def __init__(self):
        self.headers = HEADER

    def crawl(self):
        """
        get proxy from xicidaili
        :return:
        """
        for url in self.urls:
            response = requests.get(url, headers=self.headers)
            html = etree.HTML(response.text)
            for proxy in self.parse(html):
                yield proxy
