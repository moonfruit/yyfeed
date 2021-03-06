#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config

from bottle import app
from bottle import run

from yyfeed.config import plugins, db_init
from yyfeed.config import jandan_init, ttrss_init, iplaymtg_init
from yyfeed.util import app_init
from yyfeed.util.web import install


__all__ = ['app']


app_init(debug=True)
# cache_init(config.CACHE_SERVERS)
db_init(config.DB_ENGINE)
jandan_init()
ttrss_init()
iplaymtg_init()

# noinspection PyUnresolvedReferences
import yyfeed.app


install(config.PLUGINS)
install(plugins())


def main():
    run(debug=True, reloader=True)


if __name__ == '__main__':
    main()
