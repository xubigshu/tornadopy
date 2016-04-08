#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# @author   xubigshu@gmail.com
# @date     2016-1-9
#
from tornadopy import Url, route

u = Url('project_app.handlers')
urls = route(
    u(name='Index', pattern=r'/', handler='main_handler.Main'),
    u(name='BlogList', pattern=r'/BlogList', handler='main_handler.BlogList'),
    u(name='BlogNew', pattern=r'/BlogNew', handler='main_handler.BlogNew')
)

