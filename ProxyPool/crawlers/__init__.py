# encoding: utf-8
"""
@author: dawinia
@time: 2020/4/18 下午11:46
@file: __init__.py.py
@desc: 
"""
import pkgutil
import inspect
from ProxyPool.crawlers.BaseCrawler import BaseCrawler

crawlers = []

for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(module_name).load_module(module_name)
    for class_name, value in inspect.getmembers(module):
        globals()[class_name] = value
        if inspect.isclass(value) and issubclass(value, BaseCrawler) and value is not BaseCrawler:
            crawlers.append(value)

