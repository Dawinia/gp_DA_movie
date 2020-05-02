# encoding: utf-8

# Define the database class here

from sqlalchemy import Column, Integer, String, SmallInteger, Date, Float
from . import base
from logger import spider_logger as logger
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

    id = Column(Integer, primary_key=True)
    movieID = Column(Integer)  # 电影ID,
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
                setattr(self, key, items[key][0])


class MovieInfoTableTemplate(base):
    """ the movieInfo database template """

    __tablename__ = 'movieInfo'

    id = Column(Integer, primary_key=True)
    dbMovieID = Column(Integer)  # 豆瓣电影ID,
    tppMovieID = Column(Integer)  # 淘票票电影ID,
    movieName = Column(String(32))  # 电影名称,
    directors = Column(String(64))  # 导演
    writers = Column(String(128))  # 编剧
    actors = Column(String(128))  # 演员
    genre = Column(String(32))  # 类型
    area = Column(String(32))  # 地区
    duration = Column(SmallInteger)  # 电影时长
    publishedDate = Column(Date)  # 上映日期
    rateCount = Column(Integer)  # 评分人数
    doubanRate = Column(Float)  # 豆瓣评分

    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                if isinstance(items[key], str):
                    setattr(self, key, items[key])
                else:
                    setattr(self, key, items[key][0])


class PersonTableTemplate(base):
    """ the person database template """

    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(String(16))  # 名称
    url = Column(String(20))  # url
    identity = Column(String(8))  # 身份

    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key][0])


# class MovieCommentTableTemplate(base):
#     """ the movie comment database template """
#
#     __tablename__ = 'movieComment'
#
#     # TODO: 添加评论表字段
#     def __init__(self, **items):
#         for key in items:
#             if hasattr(self, key):
#                 logger.warning(f"here {key} equals to {items[key][0]}")
#                 setattr(self, key, items[key][0])
