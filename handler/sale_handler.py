__author__ = 'ping'
# -*- coding:utf-8 -*-
import tornado.web
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from table_pro import *


class SaleBaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("seller_name")


class SaleLoginHandler(SaleBaseHandler):
    """销售登录Handler，并将登录用户名及生产商代号保存到cookie中"""
    def get(self):
        self.render("sale/sale_login.html")

    def post(self):
        self.set_secure_cookie("seller_name", self.get_argument("seller_name"))
        self.set_secure_cookie("company_id", self.get_argument("company_id"))
        self.redirect("/sale_main")


class SaleExitHandler(SaleBaseHandler):
    """销售退出Handler，并将保存到cookie中的变量全部清除"""
    def get(self):
        self.clear_all_cookies()
        self.redirect("/")


class SaleActiveHandler(SaleBaseHandler):
    def post(self):
        company_id = self.get_secure_cookie("company_id")
        trace_codes = self.get_argument("trace_codes")
        db = self.application.db
        codes = dict()
        for line in trace_codes.split("\n"):
            try:
                db.query(CommodityInfo).filter(and_(CommodityInfo.companyid == company_id,
                                                    CommodityInfo.tracecode == line)).one()
                tpr = db.query(TracecodePackageRelation).filter(TracecodePackageRelation.tracecode == line).filter(
                    TracecodePackageRelation.pid.in_(db.query(PcoRelation.pid).filter_by(companyid=company_id))).one()
            except NoResultFound:
                codes[line] = "激活失败！该追溯码不存在或该产品尚未出厂..."
                continue
            if tpr.state != 0:
                codes[line] = "激活失败！该追溯码已被标记为丢失或损坏..."
            elif tpr.is_active == 1:
                codes[line] = "激活失败！该追溯码已被激活..."
            else:
                codes[line] = "激活成功！"
                tpr.is_active = 1
                tpr.time = datetime.now()
                db.add(tpr)
        db.commit()
        for (k, v) in codes.items():
            self.write(k)
            self.write('----------->')
            self.write(v)
            self.write('<br>')


class SaleMainHandler(SaleBaseHandler):
    """销售主页面Handler，先判断当前用户是否登录，登录则返回销售主页面给客户端"""
    def get(self):
        if not self.current_user:
            self.redirect("/sale_login")
            return
        self.render("sale/sale_main.html", seller_name=self.current_user)
