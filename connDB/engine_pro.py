__author__ = 'ping'
#encoding=utf-8

from sqlalchemy import create_engine
from tornado.options import define, options

define("username", default='root', help="user of database", type=str)
define("password", default=None, help="password of database", type=str)
define("ip", default='localhost', help="ip of database connnection", type=str)
define("db_port", default=3306, help="run on the given port", type=int)
define("db", default=None, help="db name", type=str)


class Engine(object):

    __password = 'ping'
    __db = 'kcdemo'
    __instance = None

    def __init__(self):
        self.__instance = None
        self.__engine = None
        self.username = options.username
        self.ip = options.ip
        self.port = options.db_port

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(Engine, cls).__new__(cls)
        return cls.__instance

    def __mysql_engine_pro(self):
        mysql_engine = create_engine('mysql://%s:%s@%s:%d/%s?charset=utf8' %
                                     (self.username, self.__password, self.ip, self.port, self.__db),
                                     encoding="utf-8", echo=True)
        self.__engine = mysql_engine

    def __sqllite_engine_pro(self):
        pass

    def __oracle_engine_pro(self):
        pass

    def get_mysql_engine(self):
        if self.__engine is None:
            self.__mysql_engine_pro()
        return self.__engine

    def get_sqllite_engine(self):
        if self.__engine is None:
            self.__sqllite_engine_pro()
        return self.__engine

    def get_oracle_engine(self):
        if self.__engine is None:
            self.__oracle_engine_pro()
        return self.__engine