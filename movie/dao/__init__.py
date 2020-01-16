# -*- coding: utf-8 -*-

# connect to your database here

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
base = declarative_base()


def get_session():
    user = settings['DATABASE_USER']
    password = settings['DATABASE_PASSWORD']
    port = settings['DATABASE_PORT']
    db_name = settings['DATABASE_NAME']
    engine = create_engine(f'mysql+pymysql://{user}:{password}@localhost:{port}/{db_name}?charset=UTF8MB4',
                           echo=True)  # 连接数据库
    session = sessionmaker(bind=engine)
    sess = session()
    return sess
