# encoding: utf-8
"""
@author: dawinia
@time: 2020/4/18 下午11:34
@file: RedisClient.py
@desc: 
"""
from random import choice

import redis
from ProxyPool.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY, MAX_SCORE, INITIAL_SCORE, MIN_SCORE
from ProxyPool.scheme.Proxy import Proxy
from ProxyPool.utils.parse import convert
from logger import proxy_logger as logger


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
        if not self.exists(proxy):
            return self.con.zadd(REDIS_KEY, {proxy.string(): score})

    def random_proxy(self) -> Proxy:
        """
        random get proxy
        :return:
        """
        proxies = self.con.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        print(proxies)
        if len(proxies):
            return convert(choice(proxies))
        proxies = self.con.zrevrange(REDIS_KEY, MIN_SCORE, MAX_SCORE)
        print(proxies)
        if len(proxies):
            return choice(convert(proxies))
        # else raise error
        raise Exception

    def deduction(self, proxy):
        """
        deduct score of proxy
        :param proxy: proxy
        :return:
        """
        score = self.con.zscore(REDIS_KEY, proxy.string())
        if score and score > MIN_SCORE:
            logger.info(f"{proxy.string()} with score {score}, deduct")
            return self.con.zincrby(REDIS_KEY, -1, proxy.string())
        else:
            logger.info(f"{proxy.string()} with score {score}, remove")
            return self.con.zrem(REDIS_KEY, proxy.string())

    def exists(self, proxy) -> bool:
        """
        judge a proxy exists or not
        :param proxy:
        :return: bool
        """
        return not self.con.zscore(REDIS_KEY, proxy.string()) is None

    def count(self):
        return self.con.zcard(REDIS_KEY)

    def max(self, proxy):
        """
        set max score to proxy
        :param proxy:
        :return:
        """
        return self.con.zadd(REDIS_KEY, {proxy.string(): MAX_SCORE})

    def batch(self, start, end):
        return convert(self.con.zrevrange(REDIS_KEY, start, end - 1))
