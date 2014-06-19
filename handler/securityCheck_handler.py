__author__ = 'ping'
# -*- coding:utf-8 -*-
import tornado.web
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from table_pro import *


class SecurityCheckMainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("security/security_check_main.html")


class CheckHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        trace_code = self.get_argument("trace_code")
        security_code = self.get_argument("security_code")
        company_id = "C1000001"
        db = self.application.db
        try:
            result = db.query(CommodityInfo).filter(and_(CommodityInfo.companyid == company_id,
                                                         CommodityInfo.tracecode == trace_code)).one()
        except NoResultFound:
            self.write("该产品追溯码不存在！")
            return
        if result.securitycode != security_code:
            self.write("该产品防伪码错误！")
        else:
            try:
                tpr = db.query(TracecodePackageRelation).filter(
                    TracecodePackageRelation.tracecode == trace_code).filter(
                        TracecodePackageRelation.pid.in_(db.query(PcoRelation.pid).filter_by(
                            companyid=company_id))).one()
            except NoResultFound:
                self.write("系统错误！")
                return
            if tpr.state != 0 or tpr.is_active == 0:
                self.write("该产品为非法劣质产品！")
                return
            elif tpr.is_check == 1:
                self.write("该产品已被查询过，如非本人操作，请检查！<br><br>")
            else:
                tpr.is_check = 1
                db.add(tpr)
                db.commit()
                self.write("该产品是正品！<br><br>")
            self.write("<table border=\"1\" align=\"center\" style=\"color: #000000; width: 400px\">"
                       "<tbody><tr><td colspan=\"2\"><span style=\"font-weight: bold\">"
                       "产品信息</span></td></tr>")
            self.write("<tr style=\"font-weight: bold; font-size: 13px; color: #696969\"><td>追溯码</td><td>")
            self.write(result.tracecode)
            self.write("</td></tr>")
            self.write("<tr style=\"font-weight: bold; font-size: 13px; color: #696969\"><td>防伪码</td><td>")
            self.write(result.securitycode)
            self.write("</td></tr>")
            self.write("<tr style=\"font-weight: bold; font-size: 13px; color: #696969\"><td>公司代号</td><td>")
            self.write(result.companyid)
            self.write("</td></tr>")
            self.write("<tr style=\"font-weight: bold; font-size: 13px; color: #696969\"><td>种类码</td><td>")
            self.write(result.sortcode)
            self.write("</td></tr>")
            self.write("<tr style=\"font-weight: bold; font-size: 13px; color: #696969\"><td>销售时间</td><td>")
            self.write(tpr.time.strftime("%Y-%m-%d %H:%M:%S"))
            self.write("</td></tr></tbody></table>")
