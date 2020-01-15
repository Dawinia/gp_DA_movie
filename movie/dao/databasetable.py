# encoding: utf-8

# Define the database class here

from sqlalchemy import Column, Integer, String, SmallInteger, Date, Float
from . import base
from movie.spiders.boxOffice_spider import logger


# class BaseTableTemplate(base):
#     """ the base database template """
#
#     def __init__(self, **items):
#         for key in items:
#             if hasattr(self, key):
#                 setattr(self, key, items[key])


class BoxOfficeTableTemplate(base):
    """ the boxOffice database template """

    __tablename__ = 'boxOffice'

    movieID = Column(Integer, primary_key=True)  # 电影ID,
    movieName = Column(String(32))  # 电影名称,
    seatRate = Column(String(5))  # 上座率,
    boxInfo = Column(Float)  # 综合票房,
    boxRate = Column(String(5))  # 票房占比,
    releaseInfo = Column(String(10))  # 上映时间,
    showInfo = Column(Integer)  # 排片场次,
    showRate = Column(String(5))  # 排片占比,
    splitBoxInfo = Column(Float)  # 分账票房,
    splitSumBoxInfo = Column(Float)  # 总分账票房,
    sumBoxInfo = Column(Float)  # 总综合票房,
    showView = Column(SmallInteger)  # 场均人次,
    crawlDate = Column(Date)  # 爬取日期
    yearRate = Column(String(13))

    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                logger.warning(f"here {key} equals to {items[key][0]}")
                setattr(self, key, items[key][0])
