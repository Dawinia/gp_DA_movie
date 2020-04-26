# encoding: utf-8
"""
@author: dawinia
@time: 2020/4/22 上午11:14
@file: tester.py
@desc: 
"""
import asyncio
import aiohttp
from ProxyPool.utils.logger import logger
from ProxyPool.scheme.Proxy import Proxy
from ProxyPool.storage.RedisClient import RedisClient
from ProxyPool.settings import TEST_TIMEOUT, TEST_BATCH, TEST_URL, TEST_VALID_STATUS
from aiohttp import ClientProxyConnectionError, ServerDisconnectedError, ClientOSError, ClientHttpProxyError
from asyncio import TimeoutError

EXCEPTIONS = (
    ClientProxyConnectionError,
    ConnectionRefusedError,
    TimeoutError,
    ServerDisconnectedError,
    ClientOSError,
    ClientHttpProxyError
)


class Tester(object):
    """
    tester for testing proxies in queue
    """

    def __init__(self):
        """
        init redis
        """
        self.redis = RedisClient()
        self.loop = asyncio.get_event_loop()

    async def test(self, proxy: Proxy):
        """
        test single proxy
        :param proxy: Proxy object
        :return:
        """
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            try:
                logger.info(f'testing {proxy.string()}')
                async with session.get(TEST_URL, proxy=f'http://{proxy.string()}', timeout=TEST_TIMEOUT,
                                       allow_redirects=False) as response:
                    if response.status in TEST_VALID_STATUS:
                        self.redis.max(proxy)
                        logger.info(f'proxy {proxy.string()} is valid, set max score')
                    else:
                        self.redis.deduction(proxy)
                        logger.info(f'proxy {proxy.string()} is invalid, decrease score')
            except EXCEPTIONS:
                self.redis.deduction(proxy)
                logger.warn(f'proxy {proxy.string()} is invalid, decrease score')
            finally:
                await session.close()

    def run(self):
        """
        test main method
        :return:
        """
        # event loop of aiohttp
        logger.info('stating tester...')
        count = self.redis.count()
        logger.info(f'{count} proxies to test')
        for i in range(0, count, TEST_BATCH):
            # start end end offset
            start, end = i, min(i + TEST_BATCH, count)
            logger.info(f'testing proxies from {start} to {end} indices')
            proxies = self.redis.batch(start, end)
            tasks = [self.test(proxy) for proxy in proxies]
            # run tasks using event loop
            self.loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    tester = Tester()
    tester.run()
