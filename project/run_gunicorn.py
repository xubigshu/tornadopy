#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# @author   xubigshu@gmail.com
# @site     http://www.51lu.me
# @date     2016-1-9
#
from tornadopy.webserver import Server
# import os

"""
run at gunicorn.
gunicorn -c gunicorn.py.conf run_gunicorn:app
tornadopy settings 写在gunicorn.conf.py中：
os.environ.setdefault('tornadopy_APP_SETTINGS', 'settings.setting')
"""

server = Server()
server.parse_command()
server.load_urls()

app = server.load_application()


