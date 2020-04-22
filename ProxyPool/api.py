# encoding: utf-8
"""
@author: dawinia
@time: 2020/4/18 下午11:56
@file: api.py
@desc: 
"""
from flask import Flask, g
from ProxyPool.storage.RedisClient import RedisClient
from ProxyPool.settings import API_HOST, API_THREADED, API_PORT

app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def hello_world():
    return 'Hello World with Flask!'


@app.route('/random')
def get_random_proxy():
    conn: RedisClient = get_conn()
    data = conn.random_proxy().string()
    return data


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED, debug=True)
