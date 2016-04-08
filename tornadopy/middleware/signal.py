#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# @author   xubigshu@gmail.com
# @date     2016-1-9
# @note     注释如下:
"""
SignalMiddleware提供在程序运行至中间件call,request,response,endcall,render几个阶段时触发信号的能力

"""
from tornadopy.signal import *


class SignalMiddleware(object):
    def process_call(self, request, clear):
        call_started.send(sender=request.__class__, request=request)

    def process_request(self, handler, clear):
        handler_started.send(sender=handler.__class__, handler=handler)

    def process_response(self, handler, clear, chunk):
        handler_response.send(sender=handler.__class__, handler=handler, chunk=chunk)

    def process_endcall(self, handler, clear):
        call_finished.send(sender=handler.__class__, handler=handler)

    def process_render(self, handler, clear, template_name, **kwargs):
        handler_render.send(sender=handler.__class__, handler=handler, template_name=template_name, kwargs=kwargs)
