__author__ = 'ping'
# -*- coding:utf-8 -*-
import os.path

import tornado
import tornado.httpserver
import tornado.web
import tornado.ioloop
import base64
import uuid
from tornado.options import options, define

import receipt_handler
import manage_handler
import sale_handler
import securityCheck_handler
import conn_db
import table_pro


define("port", default=8888, help="run on the given port", type=int)

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates")
STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", manage_handler.IndexHandler),
            (r"/receipt_login", receipt_handler.ReceiptLoginHandler),
            (r"/r_main", receipt_handler.ReceiptMainHandler),
            (r"/report_code", receipt_handler.ReportCodeHandler),
            (r"/report_box", receipt_handler.ReportBoxHandler),
            (r"/report_load", receipt_handler.ReportLoadHandler),
            (r"/report_exit", receipt_handler.ReceiptExitHandler),
            (r"/report_revoke/(.+)", receipt_handler.ReportRevokeHandler),
            (r"/sale_login", sale_handler.SaleLoginHandler),
            (r"/sale_main", sale_handler.SaleMainHandler),
            (r"/sale_exit", sale_handler.SaleExitHandler),
            (r"/sale/active", sale_handler.SaleActiveHandler),
            (r"/security_main", securityCheck_handler.SecurityCheckMainHandler),
            (r"/security_check", securityCheck_handler.CheckHandler),
            (r"/manage/receive", manage_handler.ReceiveReportHandler),
            (r"/manage/receive_box", manage_handler.ReceiveBoxReportHandler),
            (r"/manage/report", manage_handler.ReportHandler),
            (r"/manage/report_box", manage_handler.ReportBoxHandler)
        ]
        settings = dict(
            template_path=TEMPLATE_PATH,
            static_path=STATIC_PATH,
            cookie_secret=base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
            xsrf_cookies=True,
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        table_pro.TablePro()
        self.db = conn_db.session_pro()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.httpserver.HTTPServer(Application())
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()