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
    u(name='Index', pattern=r'/', handler='main_handler.Main'),
    u(name='BlogList', pattern=r'/BlogList', handler='main_handler.BlogList'),
    u(name='BlogNew', pattern=r'/BlogNew', handler='main_handler.BlogNew'),
    u(name='LoginHandler', pattern=r'/LoginHandler', handler='main_handler.LoginHandler'),
    u(name='AuthHandler', pattern=r'/AuthHandler', handler='main_handler.AuthHandler'),
    u(name='LogoutHandler', pattern=r'/LogoutHandler', handler='main_handler.LogoutHandler')
)

