# encoding: utf-8
"""
@author: dawinia
@time: 2020/4/18 下午11:36
@file: settings.py
@desc: 
"""
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = 'movie'
REDIS_KEY = 'proxies'

LOG_FILE = 'proxy.log'

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)   '
                  'Chrome/45.0.2454.101 Safari/537.36',
}
