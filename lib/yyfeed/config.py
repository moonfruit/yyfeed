#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences
from bottle.ext.sqlalchemy import SQLAlchemyPlugin
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .db import Base
from .util.cache import Cache


_plugins = []
_cache = None


def plugins():
    return tuple(_plugins)


def add_plugin(plugin):
    _plugins.append(plugin)
    return plugin


def db_init(engine=None, **kargs):
    if engine is None:
        engine = create_engine('sqlite:///:memory:', echo=True)

    if 'create' not in kargs:
        kargs['create'] = True

    if kargs['create']:
        if 'metadata' not in kargs:
            kargs['metadata'] = Base.metadata

    if 'create_session' not in kargs:
        kargs['create_session'] = scoped_session(sessionmaker())

    return add_plugin(SQLAlchemyPlugin(engine, **kargs))


def cache_init(servers):
    global _cache
    _cache = Cache(servers)
    return _cache
