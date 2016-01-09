#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# @author   xubigshu@gmail.com
# @site     http://www.51lu.me
# @date     2016-1-9
# @note     Dummy cache backend
#


from tornadopy.cache.backends.base import BaseCache, DEFAULT_TIMEOUT


class DummyCache(BaseCache):
    def __init__(self, host, *args, **kwargs):
        BaseCache.__init__(self, *args, **kwargs)

    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        return True

    def get(self, key, default=None, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        return default

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)

    def delete(self, key, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)

    def get_many(self, keys, version=None):
        return {}

    def has_key(self, key, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        return False

    def set_many(self, data, timeout=DEFAULT_TIMEOUT, version=None):
        pass

    def delete_many(self, keys, version=None):
        pass

    def clear(self):
        pass
