#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# @author   xubigshu@gmail.com
# @site     http://www.51lu.me
# @date     2016-1-9
# @note     注释如下:
"""Multi-consumer multi-producer dispatching mechanism
Originally based on pydispatch (BSD) http://pypi.python.org/pypi/PyDispatcher/2.0.1
See license.txt for original license.
"""

from dispatcher import Signal, receiver