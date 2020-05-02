# encoding: utf-8
"""
@author: dawinia
@time: 2020/5/2 下午12:09
@file: logger.py
@desc: 
"""
import logging
from scrapy.utils.project import get_project_settings
import random

settings = get_project_settings()

logging.basicConfig(
    filename=settings['BOXOFFICE_LOG_FILE'],
    level=logging.INFO,
    format='%(asctime)s -  %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class Logger:
    """
封装后的logging
    """

    def __init__(self, logger=None):
        """
            指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        """

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.INFO)
        # 创建一个handler，用于写入日志文件
        # self.log_time = time.strftime("%Y_%m_%d_")
        if logger == 'boxOfficeLogger':
            self.log_filename = settings['BOXOFFICE_LOG_FILE']
        elif logger == 'proxyPoolLogger':
            self.log_filename = settings['PROXYPOOL_LOG_FILE']

        file_handler = logging.FileHandler(self.log_filename, 'a', encoding='utf-8')  # 这个是python3的
        file_handler.setLevel(logging.INFO)

        # 再创建一个handler，用于输出到控制台
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '%(asctime)s -  %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        #  添加下面一句，在记录日志之后移除句柄
        # self.logger.removeHandler(ch)
        # self.logger.removeHandler(fh)
        # 关闭打开的文件
        file_handler.close()
        console_handler.close()

    def get_log(self):
        return self.logger


spider_logger = Logger('boxOfficeLogger').get_log()
proxy_logger = Logger('proxyPoolLogger').get_log()
