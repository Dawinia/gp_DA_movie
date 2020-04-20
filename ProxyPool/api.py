# encoding: utf-8
"""
@author: dawinia
@time: 2020/4/18 下午11:56
@file: api.py
@desc: 
"""
from flask import Flask, g
from ProxyPool.storage.RedisClient import RedisClient

app = Flask(__name__)


def get_conn():
    if hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def hello_world():
    return 'Hello World with Flask!'


@app.route('/random')
def get_random_proxy():
    conn: RedisClient = get_conn()
    return conn.random_proxy().string()


if __name__ == '__main__':
    app.run()
