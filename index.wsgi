#!/usr/bin/env python
# -*- coding: utf-8 -*-

from env import app

# noinspection PyUnresolvedReferences
from sae import create_wsgi_app
# noinspection PyUnresolvedReferences
from sae.ext.shell import ShellMiddleware

# application = create_wsgi_app(ShellMiddleware(app()))
application = create_wsgi_app(app())
