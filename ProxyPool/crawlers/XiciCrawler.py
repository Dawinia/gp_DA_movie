# encoding: utf-8
"""
@author: dawinia
@time: 2020/4/18 下午11:51
@file: XiciCrawler.py
@desc: 
"""
from random import randint

from ProxyPool.scheme.Proxy import Proxy
from ProxyPool.crawlers.BaseCrawler import BaseCrawler

BASE_URL = 'https://www.xicidaili.com/wn/{page}'


class XiciCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        start = randint(0, 5)
        self.urls = [BASE_URL.format(page=i) for i in range(start, start + 5)]

    # def crawl(self):
    #     """
    #     get proxy from xicidaili
    #     :return:
    #     """
    #     for url in self.urls:
    #         logger.debug(f"crawl url = {url}")
    #         response = requests.get(url, headers=self.headers)
    #         html = etree.HTML(response.text)
    #         for proxy in self.parse(html):
    #             yield proxy

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
            yield Proxy(host=host, port=int(port))


if __name__ == '__main__':
    crawl = XiciCrawler()
    for proxy in crawl.crawl():
        print(f"proxy: {proxy.string()}")
