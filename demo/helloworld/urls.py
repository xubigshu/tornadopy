#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# @author   xubigshu@gmail.com
# @site     http://www.51lu.me
# @date     2016-1-9
#
from tornadopy import Url, route

u = Url('helloworld.handlers')
urls = route(
    u(name='Index', pattern=r'/?', handler='main_handler.Main')
)

