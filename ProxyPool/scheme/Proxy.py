# encoding: utf-8
"""
@author: dawinia
@time: 2020/4/21 上午12:37
@file: Proxy.py
@desc: 
"""
from attr import attrs, attr


@attrs
class Proxy:
    host = attr(type=str, default=None)
    port = attr(type=int, default=None)

    def string(self):
        return f"{self.host}:{self.port}"
