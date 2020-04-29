# encoding: utf-8
"""
@author: dawinia
@time: 2020/4/29 下午5:22
@file: entry_point.py
@desc: 
"""

from scrapy.cmdline import execute

if __name__ == '__main__':
    execute(["scrapy", "crawl", "movie"])
