#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# @author   xubigshu@gmail.com
# @site     http://www.51lu.me
# @date     2016-1-9
#

from tornadopy.handler import WebHandler


class BaseHandler(WebHandler):
    """
    do some your base things
    """


class Main(BaseHandler):
    def get(self):
        welcome = "Hello,tornadopy!"
        self.render("index.html", welcome=welcome)

# model query
from ..models.main_models import Blog, User

class BlogList(BaseHandler):
    def get(self):
        this_user = self.get_argument("uid")
        # 查询，使用Q对象，或Blog.session.query(Blog).filter().all()
        blog_list = Blog.Q.filter(User.id == this_user).all()

        self.finish('ok')


class BlogNew(BaseHandler):
    def post(self):
        # 使用主库，如果没有设置主从，直接Blog.session即可，同时，User.session 等同于 Blog.session
        session = Blog.session.using_master()
        try:
            Blog.title = 'some title'
            Blog.content = 'today is good day!'
        except Exception:
            session.rollback()
        else:
            session.add(Blog)
            session.commit()

        self.finish('ok')


#下面是session的测试代码
class LoginHandler(WebHandler):
    def get(self):
        uid = self.get_argument("uid")
        self.session['userid'] = uid

        print "**************************"
        print type(self.session)
        print self.session
        print "**************************"

        self.session.set_expire(3600 * 24 * 30) #30天
        self.finish('ok')

class AuthHandler(WebHandler):
    def get(self):
        uid = self.session['userid']

        print "************************"
        print uid
        print "************************"

        

        self.finish(uid)

class LogoutHandler(WebHandler):
    def get(self):
        del self.session['userid']
        self.finish('ok')