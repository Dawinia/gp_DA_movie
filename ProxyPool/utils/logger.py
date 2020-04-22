# encoding: utf-8
"""
@author: dawinia
@time: 2020/4/22 上午10:48
@file: logger.py
@desc: 
"""

import logging
from ProxyPool.settings import LOG_FILE

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s -  %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger('proxyPoolLogger')
