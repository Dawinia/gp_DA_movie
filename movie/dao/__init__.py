# -*- coding: utf-8 -*-

# connect to your database here


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

base = declarative_base()
engine = create_engine('mysql+pymysql://root:ws.748264@localhost:3306/movie?charset=UTF8MB4', echo=True)  # 连接数据库


def get_session():
    session = sessionmaker(bind=engine)
    sess = session()
    return sess
