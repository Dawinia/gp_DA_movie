# encoding: utf-8
"""
@author: dawinia
@time: 2020/4/18 下午11:51
@file: XiciCrawler.py
@desc: 
"""
import requests
import logging
from ProxyPool.settings import LOG_FILE, HEADER
from lxml import etree
from ProxyPool.scheme import Proxy

BASE_URL = 'https://www.xicidaili.com/wn/{page}'

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.WARNING,
    format='%(asctime)s -  %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger('proxyPoolLogger')


class XiciCrawler:
    def __init__(self):
        self.urls = [BASE_URL.format(page=i) for i in range(1, 5)]
        self.headers = HEADER

    def crawl(self):
        """
        get proxy from xicidaili
        :return:
        """
        for url in self.urls:
            logger.debug(f"crawl url = {url}")
            response = requests.get(url, headers=self.headers)
            html = etree.HTML(response.text)
            for proxy in self.parse(html):
                yield proxy

    def parse(self, html) -> str:
        """
        parse the html and get proxy
        :param html:
        :return: proxy
        """
        content = html.xpath('//*[@id="ip_list"]')
        host_list = content[0].xpath('./tr/td[2]/text()')
        port_list = content[0].xpath('./tr/td[3]/text()')
        proxies = list(map(lambda x, y: (x, y), host_list, port_list))
        for host, port in proxies:
            yield Proxy(host, port)


if __name__ == '__main__':
    crawl = XiciCrawler()
    for proxy in crawl.crawl():
        print(f"proxy: {proxy}")
