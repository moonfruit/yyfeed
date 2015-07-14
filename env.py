#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config

from bottle import app
from bottle import run

from yyfeed.config import plugins, cache_init, db_init, jandan_init, ttrss_init
from yyfeed.util import app_init
from yyfeed.util.web import install


__all__ = ['app']


app_init(debug=True)
# cache_init(config.CACHE_SERVERS)
db_init(config.DB_ENGINE)
jandan_init()
ttrss_init()


# noinspection PyUnresolvedReferences
import yyfeed.app


install(config.PLUGINS)
install(plugins())


def main():
    run(debug=True, reloader=True)


if __name__ == '__main__':
    main()
