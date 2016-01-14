#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# @author   xubigshu@gmail.com
# @site     http://www.51lu.me
# @date     2016-1-9
#
import traceback
from tornado import web
from tornado import version_info
from logger import SysLogger
from middleware.manager import Manager
from tornado import httputil


class Application(web.Application):
    def __init__(self, handlers=None,
                 default_host="",
                 transforms=None,
                 wsgi=False,
                 middlewares=None,
                 **settings):

        super(Application, self).__init__(
            handlers=handlers,
            default_host=default_host,
            transforms=transforms,
            wsgi=wsgi, **settings)

        self.middleware_fac = Manager()
        if middlewares:
            self.middleware_fac.register_all(middlewares)
            self.middleware_fac.run_init(self)

        if version_info[0] > 3:
            #在版本高于4的都不是用__call__()函数处理请求了
            this = self

            class HttpRequest(httputil.HTTPServerRequest):
                def __init__(self, *args, **kwargs):
                    super(HttpRequest, self).__init__(*args, **kwargs)
                    this.middleware_fac.set_request(self)
                    try:
                        this.middleware_fac.run_call(self)
                    except Exception:
                        SysLogger.trace_logger.error(traceback.format_exc())

            httputil.HTTPServerRequest = HttpRequest

    def __call__(self, request):
        if version_info[0] < 4:
            try:
                self.middleware_fac.set_request(request)
                self.middleware_fac.run_call(request)
                return web.Application.__call__(self, request)

            except Exception, e:
                SysLogger.trace_logger.error(e)
                raise
