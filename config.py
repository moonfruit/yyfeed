#!/usr/bin/env python
# -*- coding: utf-8 -*-
from path import add_path
add_path("lib")

import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from yyfeed.util.web import exception_logger


if 'SERVER_SOFTWARE' in os.environ:
    # noinspection PyUnresolvedReferences
    from sae.const import (
        MYSQL_DB,
        MYSQL_USER,
        MYSQL_PASS,
        MYSQL_HOST,
        MYSQL_PORT,
    )

    DB_ENGINE = create_engine(URL('mysql',
                                  username=MYSQL_USER,
                                  password=MYSQL_PASS,
                                  host=MYSQL_HOST,
                                  port=MYSQL_PORT,
                                  database=MYSQL_DB,
                                  query={'charset': 'utf8'}),
                              pool_recycle=10)

    CACHE_SERVERS = None

    PLUGINS = [exception_logger]

else:
    DB_ENGINE = create_engine('mysql://root@localhost/test', pool_recycle=3600)
    # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    CACHE_SERVERS = ['localhost:11211']

    PLUGINS = []
