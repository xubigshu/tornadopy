#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# @author   xubigshu@gmail.com
# @date     2016-1-9
#

# import all model for syncdb
from models.main_models import *

from tornadopy.db.dbalchemy import Connector


def syncdb():
    for k, conn in Connector.conn_pool.items():
        conn.create_db()