# -*- coding: utf-8 -*-

# connect to your database here

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scrapy.utils.project import get_project_settings
import redis

settings = get_project_settings()
base = declarative_base()


class MySQLHelper:
    def __init__(self, user=None, pwd=None, port=None, db_name="movie"):
        self.user = user
        self.password = pwd
        self.port = port
        self.db_name = db_name
        self.engine = None

    def get_session(self):
        self.engine = create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@localhost:{self.port}/{self.db_name}?charset=UTF8MB4',
            echo=True)  # 连接数据库
        session = sessionmaker(bind=self.engine)
        sess = session()
        return sess


class RedisHelper:
    def __init__(self, host, port, pwd):
        self.host = host
        self.port = port
        self.password = pwd
        self.conn = None

    def get_conn(self):
        self.conn = redis.StrictRedis(host=self.host, port=self.port, password=self.password)
        return self.conn
