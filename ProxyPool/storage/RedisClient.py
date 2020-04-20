# encoding: utf-8
"""
@author: dawinia
@time: 2020/4/18 下午11:34
@file: RedisClient.py
@desc: 
"""
import redis
from ProxyPool.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY, MAX_SCORE, INITIAL_SCORE
from ProxyPool.scheme.Proxy import Proxy


class RedisClient:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.con = redis.StrictRedis(host=host, port=port, password=password)

    def add(self, proxy, score=INITIAL_SCORE) -> bool:
        """
        add a proxy with score
        :param score: score
        :param proxy: proxy
        :return: success or not
        """
        if not self.con.zscore(REDIS_KEY, proxy.string()):
            return self.con.zadd(REDIS_KEY, {proxy.string(): score})

    def random_proxy(self) -> Proxy:
        """
        random get proxy
        :return:
        """
        proxies = self.con.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        print(proxies)
        return proxies[0]

    def deduction(self, proxy):
        """
        deduct score of proxy
        :param proxy: proxy
        :return:
        """
        pass

    def exists(self, proxy) -> bool:
        """
        judge a proxy exists or not
        :param proxy:
        :return: bool
        """
        pass

    def count(self):
        return self.con.zcard(REDIS_KEY)
