# encoding: utf-8
"""
@author: dawinia
@time: 2020/4/22 下午1:37
@file: run.py
@desc: 
"""
import time
import multiprocessing
from ProxyPool.api import app
from ProxyPool.utils.getter import Getter
from ProxyPool.utils.tester import Tester
from ProxyPool.settings import CYCLE_GETTER, CYCLE_TESTER, API_HOST, API_THREADED, API_PORT
from logger import Logger

logger = Logger('proxyPoolLogger').getlog()


tester_process, getter_process, server_process = None, None, None


class Scheduler:
    """
    scheduler
    """

    def run_tester(self, cycle=CYCLE_TESTER):
        """
        run tester
        """
        tester = Tester()
        loop = 0
        while True:
            logger.debug(f'tester loop {loop} start...')
            tester.run()
            loop += 1
            time.sleep(cycle)

    def run_getter(self, cycle=CYCLE_GETTER):
        """
        run getter
        """
        getter = Getter()
        loop = 0
        while True:
            logger.debug(f'getter loop {loop} start...')
            getter.run()
            loop += 1
            time.sleep(cycle)

    def run_server(self):
        """
        run server for api
        """
        app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)

    def run(self):
        global tester_process, getter_process, server_process
        try:
            logger.info('starting ProxyPool...')

            tester_process = multiprocessing.Process(target=self.run_tester)
            logger.info(f'starting tester, pid {tester_process.pid}...')
            tester_process.start()

            getter_process = multiprocessing.Process(target=self.run_getter)
            logger.info(f'starting getter, pid{getter_process.pid}...')
            getter_process.start()

            server_process = multiprocessing.Process(target=self.run_server)
            logger.info(f'starting server, pid{server_process.pid}...')
            server_process.start()

            tester_process.join()
            getter_process.join()
            server_process.join()
        except KeyboardInterrupt:
            logger.info('received keyboard interrupt signal')
            tester_process.terminate()
            getter_process.terminate()
            server_process.terminate()
        finally:
            # must call join method before calling is_alive
            tester_process.join()
            getter_process.join()
            server_process.join()
            logger.info(f'tester is {"alive" if tester_process.is_alive() else "dead"}')
            logger.info(f'getter is {"alive" if getter_process.is_alive() else "dead"}')
            logger.info(f'server is {"alive" if server_process.is_alive() else "dead"}')
            logger.info('proxy terminated')


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
