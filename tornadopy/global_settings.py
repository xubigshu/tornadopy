#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# @author   xubigshu@gmail.com
# @site     http://www.51lu.me
# @date     2016-1-9
#

import os

DEBUG = True

XHEADERS = True

# tornado全局配置
TORNADO_CONF = {
    "static_path": "static",
    "xsrf_cookies": True,
    "login_url": '/login',
    "cookie_secret": "bXZ/gDAbQA+zaTxdqJwxKa8OZTbuZE/ok3doaow9N4Q=",
    "template_path": os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
    # 安全起见，可以定期生成新的cookie 秘钥，生成方法：
    # base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
}

# ###########
# 中间件     #
# ###########
MIDDLEWARE_CLASSES = (
    'tornadopy.middleware.accesslog.AccessLogMiddleware',
    'tornadopy.middleware.token.TokenMiddleware',
    'tornadopy.httpmodule.httpmodule.HttpModuleMiddleware',
)
INSTALLED_APPS = (
)
# 全局modules配置
COMMON_MODULES = (
    # 'module限定名',
)
# 路由modules，针对某个路由或某些路由起作用
ROUTE_MODULES = {
    # {'路由名称或正则':['module限定名','!被排除的module限定名']}
}
###########
# 缓存配置 #
###########
CACHES = {
    'default': {
        'BACKEND': 'tornadopy.cache.backends.localcache.LocMemCache',
        'LOCATION': 'process_cache',
        'OPTIONS': {
            'MAX_ENTRIES': 10000,
            'CULL_FREQUENCY': 3
        }
    },
    'default_memcache': {
        'BACKEND': 'tornadopy.cache.backends.memcached.MemcachedCache',
        'LOCATION': [
            '127.0.0.1:11211'
        ],
        'TIMEOUT': 300
    },
    'dummy': {
        'BACKEND': 'tornadopy.cache.backends.dummy.DummyCache'
    },
    'default_redis': {
        'BACKEND': 'tornadopy.cache.backends.rediscache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        'OPTIONS': {
            'DB': 0,
            'PARSER_CLASS': 'redis.connection.DefaultParser',
            'POOL_KWARGS': {
                'socket_timeout': 2,
                'socket_connect_timeout': 2
            },
            'PING_INTERVAL': 120  # 定时ping redis连接池，防止被服务端断开连接（s秒）
        }
    },

}


#################
# 本地化翻译文件地址#
#################

TRANSLATIONS = False  # 是否开启国际化
TRANSLATIONS_CONF = {
    'translations_dir': os.path.join(os.path.dirname(__file__), 'translations'),
    'locale_default': 'zh_CN',
    'use_accept_language': True
}


# 白名单未开启，如需使用，请用元祖列出白名单ip
WHITELIST = False
#######
# WHITELIST = (
#     '127.0.0.1',
# '127.0.0.2',
# )

#tornado日志功能配置
LOGGING_DIR = 'logs/'
LOGGING = (
    {
        'name': 'tornado',
        'level': 'INFO',
        'log_to_stderr': False,
        'when': 'midnight',
        'interval': 1,
        'filename': 'tornado.log'
    },
    {
        'name': 'tornadopy.tracelog',
        'level': 'ERROR',
        'log_to_stderr': False,
        'when': 'midnight',
        'interval': 1,
        'formatter': '%(message)s',
        'filename': 'tornadopy_trace_log.log'
    },
    {
        'name': 'tornadopy.accesslog',
        'level': 'INFO',
        'log_to_stderr': True,
        'when': 'midnight',
        'interval': 1,
        'formatter': '%(message)s',
        'filename': 'tornadopy_access_log.log'
    },
    {
        'name': 'tornadopy.infolog',
        'level': 'INFO',
        'log_to_stderr': False,
        'when': 'midnight',
        'interval': 1,
        'filename': 'tornadopy_info_log.log'
    }
)

IPV4_ONLY = True


#开启session支持
SESSION = {
    'session_cache_alias': 'default',  # 'session_loccache',对应cache配置
    'session_name': '__TORNADOID',
    'cookie_domain': '',
    'cookie_path': '/',
    'expires': 0,  # 24 * 60 * 60, # 24 hours in seconds,0代表浏览器会话过期
    'ignore_change_ip': False,
    'httponly': True,
    'secure': False,
    'secret_key': 'fLjUfxqXtfNoIldA0A0J',
    'session_version': 'EtdHjDO1'
}

# 开启token支持，该模式只支持redis，对于其他几种缓存，其他几种缓存不支持
TOKEN = {
    'token_cache_alias': 'default_redis',  # 此处必须是 default_redis
    'ignore_change_ip': False,
    'token_timeout': 2592000,
    'secret_key': 'fLjUfxqXtfNoIldA0A0J',
    'token_version': ''
}


#配置模版引擎
#引入相应的TemplateLoader即可
#若使用自带的请给予None
#支持mako和jinja2
#mako设置为tornadopy.template.mako_loader.MakoTemplateLoader
#jinj2设置为tornadopy.template.jinja2_loader.Jinja2TemplateLoader
#初始化参数请参照jinja的Environment或mako的TemplateLookup,不再详细给出
TEMPLATE_CONFIG = {
    'template_engine': None,
    #模版路径由tornadopy.handler中commonhandler重写，无需指定，模版将存在于每个应用的根目录下
    'filesystem_checks': True,  #通用选项
    'cache_directory': '../_tmpl_cache',  #模版编译文件目录,通用选项
    'collection_size': 50,  #暂存入内存的模版项，可以提高性能，mako选项,详情见mako文档
    'cache_size': 0,  #类似于mako的collection_size，设定为-1为不清理缓存，0则每次都会重编译模板
    'format_exceptions': False,  #格式化异常输出，mako专用
    'autoescape': False  #默认转义设定，jinja2专用

}


# 数据库连接字符串，
# 元祖，每组为n个数据库连接，有且只有一个master，可配与不配slave
DATABASE_CONNECTION = {
    'default': {
        'connections': [{
                            'ROLE': 'master',
                            'DRIVER': 'mysql+mysqldb',
                            'UID': 'root',
                            'PASSWD': '',
                            'HOST': '',
                            'PORT': 3306,
                            'DATABASE': '',
                            'QUERY': {"charset": "utf8"}

                        },
                        {
                            'ROLE': 'slave',
                            'DRIVER': 'mysql+mysqldb',
                            'UID': 'root',
                            'PASSWD': '',
                            'HOST': '',
                            'PORT': 3306,
                            'DATABASE': '',
                            'QUERY': {"charset": "utf8"}

                        }]
    }
}
# 每个定时对db进行一次ping操作，防止mysql gone away
PING_DB = 300  # (s秒)
# 每次取出ping多少个连接
PING_CONN_COUNT = 5
# sqlalchemy配置，列出部分，可自行根据sqlalchemy文档增加配置项
# 该配置项对所有连接全局共享
SQLALCHEMY_CONFIGURATION = {
    'sqlalchemy.connect_args': {
        'connect_timeout': 3
    },
    'sqlalchemy.echo': False,
    'sqlalchemy.max_overflow': 10,
    'sqlalchemy.echo_pool': False,
    'sqlalchemy.pool_timeout': 5,
    'sqlalchemy.encoding': 'utf-8',
    'sqlalchemy.pool_size': 5,
    'sqlalchemy.pool_recycle': 3600,
    'sqlalchemy.poolclass': 'QueuePool'  # 手动指定连接池类
}