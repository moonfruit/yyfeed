#!/usr/bin/env python
# -*- coding: utf-8 -*-

from env import app
# noinspection PyUnresolvedReferences
from sae import create_wsgi_app

application = create_wsgi_app(app())
