# -*- coding:utf-8 -*-
import tornado.web
from sqlalchemy import and_
from table_pro import *


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("manager")


class IndexHandler(BaseHandler):
    def get(self):
        self.render("index.html")


class ReceiveReportHandler(BaseHandler):
    """对缺货上报请求进行处理Handler，返回处理结果页面给客户端
    1、先判断订单号是否存在；
    2、订单号存在，依次判断箱号是否存在于该订单号下；
    3、箱号存在，依次查询箱号对应的单品追溯码；
    4、将查询结果返回。"""
    def post(self):
        receipt_name = self.get_argument("receipt_name")
        company_id = self.get_argument("company_id")
        transport_id = self.get_argument("transport_id")
        barcode = self.get_argument("barcode")
        db = self.application.db
        p = db.query(PcoRelation.pid).filter(PcoRelation.oid.in_(db.query(SortInfo.oid).filter_by(
            transportid=transport_id))).filter(PcoRelation.companyid == company_id)
        if not list(p):
            self.render("manage/report_error.html")
        else:
            trace_codes = dict()
            for line in barcode.split("\r\n"):
                pi = db.query(PackageInfo).filter(PackageInfo.pid.in_(p)).filter(
                    PackageInfo.barcode == line).first()
                if pi and pi.state is 0:
                    trace_codes[line] = list(db.query(TracecodePackageRelation).filter_by(pid=pi.pid))
                else:
                    trace_codes[line] = [()]
            self.render("manage/report_code_result.html", transport_id=transport_id, receipt_name=receipt_name,
                        company_id=company_id, result=trace_codes)


class ReceiveBoxReportHandler(BaseHandler):
    """对缺箱上报请求进行处理Handler，返回处理结果页面给客户端
    1、先判断订单号是否存在；
    2、订单号存在，查询该订单下的所有箱号信息
    4、将查询结果返回。"""
    def post(self):
        receipt_name = self.get_argument("receipt_name")
        company_id = self.get_argument("company_id")
        transport_id = self.get_argument("transport_id")
        db = self.application.db
        p = db.query(PcoRelation.pid).filter(PcoRelation.oid.in_(db.query(SortInfo.oid).filter_by(
            transportid=transport_id))).filter(PcoRelation.companyid == company_id)
        if not list(p):
            self.render("manage/report_error.html")
        else:
            result = []
            for pi in list(p):
                b = db.query(PackageInfo).filter_by(pid=pi.pid).first()
                result.append(b)
            self.render("manage/report_box_result.html", transport_id=transport_id, receipt_name=receipt_name,
                        company_id=company_id, result=result)


class ReportBoxHandler(BaseHandler):
    def post(self):
        pids = self.get_argument("pids").split(",")
        db = self.application.db
        for pid in pids:
            p = db.query(PackageInfo).filter_by(pid=pid).first()
            p.state = 1
            db.add(p)
        db.commit()


class ReportHandler(BaseHandler):
    """对上报的缺货进行处理Handler，返回处理结果页面给客户端"""
    def post(self):
        trace_codes = self.get_argument("trace_codes").split(",")
        company_id = self.get_argument("company_id")
        reporter = self.get_argument("reporter")
        db = self.application.db
        for code in trace_codes:
            p = db.query(TracecodePackageRelation).filter(TracecodePackageRelation.tracecode == code).filter(
                TracecodePackageRelation.pid.in_(db.query(PcoRelation.pid).filter_by(companyid=company_id))).first()
            if p and p.state == 0:
                o = db.query(SortInfo).filter(SortInfo.oid.in_(db.query(PcoRelation.oid).filter(
                    and_(PcoRelation.companyid == company_id, PcoRelation.pid == p.pid)))).first()
                barcode = db.query(PackageInfo).filter_by(pid=p.pid).first()
                db.add(ReportInfo(None, reporter, barcode.barcode, o.transportid, company_id, code, datetime.now()))
                p.state = 1
                db.add(p)
        db.commit()