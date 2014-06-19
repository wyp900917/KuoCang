__author__ = 'ping'
# -*- coding:utf-8 -*-
import tornado.web
import tornado.httpclient
from sqlalchemy import and_
from table_pro import *


class ReceiptBaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("receipt_name")


class ReceiptLoginHandler(ReceiptBaseHandler):
    """收货登录Handler，并将登录用户名及生产商代号保存到cookie中"""
    def get(self):
        self.render("receipt/receipt_login.html")

    def post(self):
        self.set_secure_cookie("receipt_name", self.get_argument("receipt_name"))
        self.set_secure_cookie("company_id", self.get_argument("company_id"))
        self.redirect("/r_main")


class ReceiptExitHandler(ReceiptBaseHandler):
    """收货退出Handler，并将保存到cookie中的变量全部清除"""
    def get(self):
        self.clear_all_cookies()
        self.redirect("/")


class ReceiptMainHandler(ReceiptBaseHandler):
    """收货主页面Handler，先判断当前用户是否登录，登录则返回收货主页面给客户端"""
    def get(self):
        if not self.current_user:
            self.redirect("/receipt_login")
            return
        self.render("receipt/receipt_main.html", receipt_name=self.current_user,
                    company_id=self.get_secure_cookie("company_id"))


class ReportCodeHandler(ReceiptBaseHandler):
    """上报页面Handler，先判断当前用户是否登录，登录则返回上报页面给客户端"""
    def get(self):
        if not self.current_user:
            self.redirect("/receipt_login")
            return
        self.render("receipt/report_code.html", receipt_name=self.current_user,
                    company_id=self.get_secure_cookie("company_id"))


class ReportBoxHandler(ReceiptBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/receipt_login")
            return
        self.render("receipt/report_box.html", receipt_name=self.current_user,
                    company_id=self.get_secure_cookie("company_id"))


class ReportLoadHandler(ReceiptBaseHandler):
    """上报查看页面Handler，先判断当前用户是否登录，登录则返回上报页面给客户端"""
    def get(self):
        reporter = self.current_user
        company_id = self.get_secure_cookie("company_id")
        if not reporter:
            self.redirect("/receipt_login")
            return
        db = self.application.db
        result = db.query(ReportInfo).filter(and_(ReportInfo.reporter == reporter,
                                                  ReportInfo.companyid == company_id)).order_by(ReportInfo.time).all()
        result.reverse()
        self.render("receipt/report_load.html", reporter=reporter, result=result)


class ReportRevokeHandler(ReceiptBaseHandler):
    """上报撤销页面Handler，处理结束后返回到上报结果页面"""
    def get(self, rid):
        db = self.application.db
        p = db.query(ReportInfo).filter_by(rid=rid).first()
        t = db.query(TracecodePackageRelation).filter(and_(TracecodePackageRelation.tracecode == p.tracecode,
                                                           TracecodePackageRelation.pid.in_(db.query(PcoRelation.pid)
                                                           .filter_by(companyid=p.companyid)))).first()
        t.state = 0
        db.add(t)
        db.delete(p)
        db.commit()
        self.redirect("/report_load")