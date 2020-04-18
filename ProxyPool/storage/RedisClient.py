# encoding: utf-8
"""
@author: dawinia
@time: 2020/4/18 下午11:34
@file: RedisClient.py
@desc: 
"""
import redis
from ProxyPool.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY


class RedisClient:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.con = redis.StrictRedis(host=host, port=port, password=password)

    def add(self, score, proxy) -> bool:
        """
        add a proxy with score
        :param score: score
        :param proxy: proxy
        :return: success or not
        """
        if not self.con.zscore(REDIS_KEY, proxy):
            return self.con.zadd(REDIS_KEY, score, proxy)

    def random_proxy(self):
        """
        random get proxy
        :return:
        """
        pass

    def deduction(self, proxy):
        """
        deduct score of proxy
        :param proxy: proxy
        :return:
        """
        pass

    def exists(self, proxy):
        """
        judge a proxy exists or not
        :param proxy:
        :return: bool
        """
        pass
