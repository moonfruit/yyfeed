#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    import cPickle as pickle
except ImportError:
    import pickle

import os.path


class FileCache(dict):
    def __init__(self, filename):
        self.filename = os.path.abspath(filename)

        try:
            self.update(pickle.load(open(self.filename)))
        except:
            pass

    def __setitem__(self, key, value):
        super(FileCache, self).__setitem__(key, value)
        pickle.dump(self, open(self.filename, 'w'))

    def set(self, key, value):
        self.__setitem__(key, value)

    def get_stats(self):
        pass


try:
    import pylibmc as memcache

except ImportError:
    import memcache


class Cache(object):
    def __init__(self, servers=None, default='.cache', **kargs):
        if servers is None:
            self.cache = memcache.Client(**kargs)
        else:
            self.cache = memcache.Client(servers, **kargs)

        if not self.cache.get_stats():
            self.cache = FileCache(default)

    def __getitem__(self, key):
        return self.cache.get(key)

    def __setitem__(self, key, value):
        self.cache.set(key, value)

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache.set(key, value)
