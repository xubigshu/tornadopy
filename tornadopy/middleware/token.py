#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# @author   xubigshu@gmail.com
# @date     2016-1-9
# @note     注释如下:
"""
token中间件,只支持redis
1.这部分功能是整合之前代码的token功能进来。
"""
import os
import time
import re
import uuid
import hmac
import json
import hashlib

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


token_parameters = storage({
    'token_cache_alias': 'default_redis',  # 此处必须是 default_redis
    'ignore_change_ip': False,
    'token_timeout': 2592000,
    'secret_key': 'fLjUfxqXtfNoIldA0A0J',
    'token_version': ''
})


class TokenMiddleware(object):
    _cachestore = None
    _tokenManager = None
    token = None

    def process_init(self, application):
        self._cachestore = (caches[settings.TOKEN.token_cache_alias]).get_old_redis()

        self.config = storage(token_parameters)
        if settings.TOKEN:
            self.config.update(settings.TOKEN)

        self._tokenManager = TokenManager(self._cachestore, self.config["secret_key"])


    def process_request(self, handler, clear):
        token = Token(self._tokenManager, handler, self.config)
        handler.token = token



class TokenData(dict):
    def __init__(self, tokenID):
        self.tokenID = tokenID
     
class Token(TokenData):
    def __init__(self, token_manager, request_handler, config):
        self.token_manager = token_manager
        self.request_handler = request_handler
        
        self.config = config

        try:
            current_token = self.token_manager.get(request_handler)
        except Exception, e:
            raise ValueError("get token info from request_handler failed")

        #------------------------保存的token信息:begin-----------------------------#
        self._data = {}
        self._data.update(current_token)
        # for key, data in current_token.iteritems():
        #     self._data[key] = data

        #将客户端的ip记录下来，用于将变化的ip的登录状态给登出
        self._data['remote_ip'] = request_handler.request.remote_ip

        self.tokenID = current_token.tokenID
        #------------------------保存的token信息:end------------------------------#

    

    #------下面是一些接口方法，供外部使用token-------------------#

    #保存token信息的方法
    def save(self, tmp_data):
        self._data.update(tmp_data)
        return self.token_manager.set(self, self.config["token_timeout"])

    #根据tokenID，查找token的方法
    def fetch(self,tokenID):
        tokenData = self.token_manager._fetch(tokenID)
        return tokenData["userID"]
    
    #根据参数，查找对应的参数，否则抛出异常。
    def get_current_parameter(self, parameter):
        #此处的get方法调用的是字典的get方法,下同
        _value = None
        try:
            _value = self._data.get(parameter)
        except Exception, e:
            raise ValueError("parameter '%s' not found" % parameter)
        return _value


    def get_current_user(self):
        return self._data.get("userID")

    def get_current_authCode(self):
        return self._data.get("authCode")

    def get_current_user_name(self):
        return self._data.get("userName")

    def get_current_authToken(self):
        return self._data.get("authToken")

    #定义一个登陆权限认证的装饰器,暂时还没想好怎么使用这个装饰器比较好。先留这儿，不用吧
    def login_required(f):
        def _wrapper(self,*args, **kwargs):
            logged = self.get_current_user()
            if logged == None:
                result = {"code":-1,"reason":"tokenID invalid"}
                data = {"result":result}
                self.set_header("Content-Type", "application/json; charset=UTF-8")
                self.write(json.dumps(data))
                self.finish()
            else:
                ret = f(self,*args, **kwargs)
        return _wrapper


class TokenManager(object):
    '''
    #--- TokenManager中的方法不能在接口中调用。
    '''
    def __init__(self, tmp_store, secret):
        self.redis = tmp_store
        self.secret = secret
    
    def _fetch(self, tokenID):
        try:
            token_data = raw_data = self.redis.get(tokenID)
            if raw_data != None:
                #self.redis.setex(tokenID, self.token_timeout, raw_data)
                token_data = json.loads(raw_data)

            if type(token_data) == type({}):
                return token_data
            else:
                return {}
        except IOError:
            return {}


    def getInfoByUserName(self, userName):
        '''
        该方法用于根据提供的userName,先得到对应的token信息
        '''
        tmpTokenID = None
        tmpTokenID = self.redis.hget("onlineUser", userName)
        if self.redis.exists(tmpTokenID):
            token_data = self._fetch(tmpTokenID)
            token = {}
            for key, data in token_data.iteritems():
                token[key] = data
            return token["pushUdid"],token["clientOS"]
        else:
            return None,None


    def get(self, request_handler = None):
        if (request_handler == None):
            tokenID = None
        else:
            tokenID = request_handler.get_argument("tokenID", None)
        
        if tokenID == None:
            token_exists = False
            tokenID = -1
        else:
            if self.redis.exists(tokenID) == 1:
                token_exists = True
            else:
                token_exists = False
            
        
        token = TokenData(tokenID)
        if token_exists:
            token_data = self._fetch(tokenID)
            for key, data in token_data.iteritems():
                token[key] = data
        return token
    
    def set(self, token, expiresTime):
        tmp_token = token._data
        if expiresTime is None:
            expiresTime = self.token_timeout
        token_data = json.dumps(dict(tmp_token.items()))
        tmpTokenID = self.redis.hget("onlineUser", tmp_token["userName"])
        if self.redis.exists(tmpTokenID):
            token.tokenID = tmpTokenID
            self.redis.setex(token.tokenID, expiresTime, token_data)
            return token.tokenID
        else:
            token.tokenID = self._generate_id()
            self.redis.setex(token.tokenID, expiresTime, token_data)

            self.redis.hset("onlineUser", tmp_token["userName"], token.tokenID)
            return token.tokenID


    def _generate_id(self):
        newID = hashlib.sha256(self.secret + str(uuid.uuid4()))

        return newID.hexdigest()

    def _generate_hmac(self, tokenID):
        return hmac.new(tokenID, self.secret, hashlib.sha256).hexdigest()

    def expired(self, tokenID):
        """
        强制过期
        :return:None
        """
        self.redis.delete(tokenID)
