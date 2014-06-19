__author__ = 'ping'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, BOOLEAN, ForeignKey, DateTime
from datetime import datetime
from engine_pro import Engine

Base = declarative_base()


class CommodityInfo(Base):
    __tablename__ = 'commodity_info'

    tracecode = Column(String(50), primary_key=True)
    companyid = Column(String(50), index=True, primary_key=True)
    securitycode = Column(String(50), nullable=False)
    sortcode = Column(String(50), nullable=False)

    def __init__(self, tracecode, securitycode, companyid, sortcode):
        self.tracecode = tracecode
        self.securitycode = securitycode
        self.companyid = companyid
        self.sortcode = sortcode

    def __repr__(self):
        return "<CommodityInfo('%s','%s','%s','%s')>" \
               % (self.tracecode, self.securitycode, self.companyid, self.sortcode)


class PackageInfo(Base):
    __tablename__ = 'package_info'

    pid = Column(Integer, primary_key=True, autoincrement=True)
    barcode = Column(String(50))
    state = Column(Integer)

    def __init__(self, pid, barcode, state):
        self.pid = pid
        self.barcode = barcode
        self.state = state

    def __repr__(self):
        return "<PackageInfo('%s', '%s', '%d')>" % (self.pid, self.barcode, self.state)


class SortInfo(Base):
    __tablename__ = 'sort_info'

    oid = Column(Integer, primary_key=True, autoincrement=True)
    transportid = Column(String(50))
    orderid = Column(String(50))
    agentid = Column(String(50))
    agentname = Column(String(50))

    def __init__(self, oid, transportid, orderid, agentid, agentname):
        self.oid = oid
        self.transportid = transportid
        self.orderid = orderid
        self.agentid = agentid
        self.agentname = agentname

    def __repr__(self):
        return "<SortInfo('%d', '%s', '%s', '%s', '%s')>" \
               % (self.oid, self.transportid, self.orderid, self.agentid, self.agentname)


class TracecodePackageRelation(Base):
    __tablename__ = 'tracecode_package_relation'

    tracecode = Column(String(50), ForeignKey('commodity_info.tracecode'), primary_key=True)
    pid = Column(Integer, ForeignKey('package_info.pid'), primary_key=True)
    state = Column(Integer)
    time = Column(DateTime, default=None)
    is_check = Column(BOOLEAN, default=False)
    is_active = Column(BOOLEAN, default=False)

    def __init__(self, tracecode, pid, state, time, is_check, is_active):
        self.tracecode = tracecode
        self.pid = pid
        self.state = state
        self.time = time
        self.is_check = is_check
        self.is_active = is_active

    def __repr__(self):
        return "TracecodePackageRelation('%s', '%d', '%d', '%s', '%s', '%s')" \
               % (self.tracecode, self.pid, self.state, self.time, self.is_check, self.is_active)


class PcoRelation(Base):
    __tablename__ = 'pco_relation'

    companyid = Column(String(50), ForeignKey('commodity_info.companyid'), primary_key=True)
    pid = Column(Integer, ForeignKey('package_info.pid'), primary_key=True)
    oid = Column(Integer, ForeignKey('sort_info.oid'))

    def __init__(self, companyid, pid, oid):
        self.companyid = companyid
        self.pid = pid
        self.oid = oid

    def __repr__(self):
        return "<PcoRelation('%s', '%d', '%d')>" % (self.companyid, self.pid, self.oid)


class ReportInfo(Base):
    __tablename__ = 'report_info'

    rid = Column(Integer, primary_key=True, autoincrement=True)
    reporter = Column(String(50))
    barcode = Column(String(50))
    transportid = Column(String(50))
    companyid = Column(String(50), ForeignKey('commodity_info.companyid'))
    tracecode = Column(String(50), ForeignKey('commodity_info.tracecode'))
    time = Column(DateTime, default=datetime.now())

    def __init__(self, rid, reporter, barcode, transportid, companyid, tracecode, time):
        self.rid = rid
        self.reporter = reporter
        self.barcode = barcode
        self.transportid = transportid
        self.companyid = companyid
        self.tracecode = tracecode
        self.time = time

    def __repr__(self):
        return "<ReportInfo('%d', '%s', '%d', '%d', '%s', '%s', '%s')>" % \
               (self.rid, self.reporter, self.barcode, self.transportid, self.companyid, self.tracecode, self.time)


class TablePro(object):
    __instance = None

    def __init__(self):
        self.__instance = None
        Base.metadata.create_all(Engine().get_mysql_engine())
        print('-----------------Table create!!!')

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(TablePro, cls).__new__(cls)
        return cls.__instance
