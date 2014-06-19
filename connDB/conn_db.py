__author__ = 'ping'
#encoding=utf-8

from engine_pro import Engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()


def session_pro():
    engine = Engine().get_mysql_engine()
    Session.configure(bind=engine)
    session = Session()
    return session



