# encoding: utf-8

# Define the database class here

from sqlalchemy import Column, Integer, String, Float, SmallInteger, Date
from . import base


class BaseTableTemplate(base):
    """ the base database template """
    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])


class BoxOfficeTableTemplate(BaseTableTemplate):
    """ the boxOffice database template """

    __table_name__ = 'boxOffice'

    movie_id = Column(Integer, primary_key=True)  # 电影ID,
    movie_name = Column(String(32))  # 电影名称,
    movie_seatRate = Column(String(5))  # 上座率,
    movie_boxInfo = Column(Float)  # 综合票房,
    movie_boxRate = Column(String(5))  # 票房占比,
    movie_releaseInfo = Column(String(10))  # 上映时间,
    movie_showInfo = Column(SmallInteger)  # 排片场次,
    movie_showRate = Column(String(5))  # 排片占比,
    movie_splitBoxInfo = Column(Float)  # 分账票房,
    movie_splitSumBoxInfo = Column(Float)  # 总分账票房,
    movie_sumBoxInfo = Column(Float)  # 总综合票房,
    movie_showView = Column(SmallInteger)  # 场均人次,
    crawl_date = Column(Date)  # 爬取日期
