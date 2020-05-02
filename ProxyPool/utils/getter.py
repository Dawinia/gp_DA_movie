# encoding: utf-8
"""
@author: dawinia
@time: 2020/4/18 下午11:49
@file: getter.py
@desc: 
"""
import requests
from ProxyPool.storage.RedisClient import RedisClient
from ProxyPool.crawlers import crawlers
from logger import Logger

logger = Logger('proxyPoolLogger').getlog()


class Getter:
    def __init__(self):
        self.con = RedisClient()
        self.crawlers = [crawler() for crawler in crawlers]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        }
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
            'push_noty_num': '0', 'push_doumail_num': '0'
        }

    def full(self) -> bool:
        return self.con.count() >= 1000

    def run(self):
        def usable(proxy) -> bool:
            proxies = {'https': 'https://' + proxy}
            try:
                if requests.get('https://movie.douban.com/', proxies=proxies, cookies=self.cookies, timeout=2, headers=self.headers).status_code == 200:
                    return True
            except requests.exceptions.ProxyError:
                logger.error(f"proxy error with {proxy}")
            except requests.exceptions.ConnectTimeout:
                logger.error(f"ConnectTimeout with {proxy}")
            return False

        if self.full():
            return
        for crawler in self.crawlers:
            for proxy in crawler.crawl():
                if self.con.add(proxy):
                    logger.info(f"proxy {proxy.string()} been added")


if __name__ == '__main__':
    getter = Getter()
    getter.run()
