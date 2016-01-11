#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# @author   xubigshu@gmail.com
# @site     http://www.51lu.me
# @date     2016-1-9
# @note     注释如下:
"""
token中间件,支持disk，进程内缓存cache,memcache
sessioin过期策略分为三种情形：
1.固定时间过期，例如10天内没有访问则过期，timeout=xxx
    *cookie策略：每次访问时设置cookie为过期时间
    *缓存策略：每次访问设置缓存失效时间为固定过期时间
2.会话过期，关闭浏览器即过期timeout=0
    *cookie策略：岁浏览器关闭而过期
    *缓存策略：设置缓存失效期为1天，每次访问更新失效期，如果浏览器关闭，则一天后被清除

3.永不过期(记住我)
    *cookie策略：timeout1年
    *缓存策略：1年
"""
import os
import time
import re

try:
    import hashlib

    sha1 = hashlib.sha1
except ImportError:
    import sha

    sha1 = sha.new

from tornadopy.storage import storage
from tornadopy.utils import safestr
from tornadopy.settings_manager import settings
from tornadopy.cache import caches

rx = re.compile('^[0-9a-fA-F]+$')


class tokenMiddleware(object):
    _cachestore = None
    token = None

    def process_init(self, application):
        self._cachestore = caches[settings.token.token_cache_alias]

    def process_request(self, handler, clear):
        token = tokenManager(handler, self._cachestore, settings.token)
        token.load_token()
        handler.token = token

    def process_response(self, handler, clear, chunk):
        if hasattr(handler, "token"):
            handler.token.save()
            del handler.token


_DAY1 = 24 * 60 * 60
_DAY30 = _DAY1 * 30

token_parameters = storage({
    'token_name': '__TORNADOSSID',
    'cookie_domain': None,
    'cookie_path': '/',
    'expires': 0,  # 24 * 60 * 60, # 24 hours in seconds
    'ignore_change_ip': False,
    'httponly': True,
    'secure': False,
    'secret_key': 'fLjUfxqXtfNoIldA0A0J',
    'token_version': ''
})


class tokenManager(object):
    _killed = False

    def __init__(self, handler, store, config=None):
        self._get_cookie = handler.get_cookie
        self._set_cookie = handler.set_cookie
        self.remote_ip = handler.request.remote_ip
        self.store = store
        self.config = storage(token_parameters)
        if config:
            self.config.update(config)

        self._data = {}

    def __contains__(self, key):
        return key in self._data

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data.get(key, None)

    def __delitem__(self, key):
        del self._data[key]

    def get(self, key, default=None):
        return self._data.get(key, default)

    def load_token(self):
        """
        加载token
        :return:
        """
        self.tokenid = self._get_cookie(self.config.token_name)

        if self.tokenid and not self._valid_token_id(self.tokenid):
            self.expired()

        if self.tokenid:
            if self.tokenid in self.store:
                expires, _data = self.store.get(self.tokenid)
                self._data.update(_data)
                self.config.expires = expires
            self._validate_ip()

        if not self.tokenid:
            self.tokenid = self._create_tokenid()

        self._data['remote_ip'] = self.remote_ip

    def save(self):
        if not self._killed:
            httponly = self.config.httponly
            secure = self.config.secure
            expires = self.config.expires  # 单位:秒
            cache_expires = expires
            if expires == 0:
                # 过期时间为0时，对于tornado来说，是会话有效期，关闭浏览器失效，但是
                # 对于cache缓存而言，无法及时捕获会话结束状态，鉴于此，将cache的缓存设置为一天
                # cache在每次请求后会清理过期的缓存
                cache_expires = _DAY1

            if not secure:
                secure = ''

            if not httponly:
                httponly = ''
            set_expire = 0 if expires == 0 else time.time() + expires
            self._set_cookie(
                self.config.token_name,
                self.tokenid,
                domain=self.config.cookie_domain or '',
                expires=set_expire,
                path=self.config.cookie_path,
                secure=secure,
                httponly=httponly)

            self.store.set(self.tokenid, (expires, self._data), cache_expires)

        else:
            self._set_cookie(self.config.token_name, self.tokenid, expires=-1)
            self.store.delete(self.tokenid)
            self.tokenid = None
            self._killed = False

    def _valid_token_id(self, token_id):
        """
        验证tokenid格式
        :return:bool
        """
        if token_id:
            sess = token_id.split('|')
            if len(sess) > 1:
                return rx.match(sess[0]) and sess[1] == self.config.token_version

    def expired(self):
        """
        强制过期
        :return:None
        """
        self._killed = True
        self.save()

    def _create_tokenid(self):
        rand = os.urandom(16)
        now = time.time()
        secret_key = self.config.secret_key
        token_id = sha1("%s%s%s%s" % (rand, now, safestr(self.remote_ip), secret_key))
        token_id = token_id.hexdigest()
        return str(token_id).upper() + '|' + self.config.token_version

    def _validate_ip(self):
        if self.tokenid and self._data.get('remote_ip', None) != self.remote_ip:
            if not self.config.ignore_change_ip:
                return self.expired()

    def set_expire(self, expires):
        self.config.expires = expires
        self.save()
