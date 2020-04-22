# encoding: utf-8
"""
@author: dawinia
@time: 2020/4/22 下午2:01
@file: parse.py
@desc: 
"""
import re
from ProxyPool.scheme.Proxy import Proxy
import copy


def is_valid_proxy(data):
    """
    is data is valid proxy format
    :param data:
    :return:
    """
    print(f"1.{data} = {type(data)}")
    return re.match('\d+\.\d+\.\d+\.\d+\:\d+', data)


def convert(data):
    """
    convert list of str to valid proxies or proxy
    :param data:
    :return:
    """
    if not data:
        return None
    # if list of proxies
    if isinstance(data, list):
        result = []
        for item in data:
            # skip invalid item
            item = item.strip()
            print(f"2.{item} = {type(item)}")
            data = copy.deepcopy(item)
            if not is_valid_proxy(data.decode()):
                continue
            # item = item.encode()
            if isinstance(item, bytes):
                print(f"3.{item} = {type(item)}")
                host, port = item.split(b':')
                result.append(Proxy(host=host, port=int(port)))
        return result
    if isinstance(data, str) and is_valid_proxy(data):
        host, port = data.split(':')
        return Proxy(host=host, port=int(port))

