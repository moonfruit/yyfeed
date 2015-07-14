#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from bottle import HTTPResponse, HTTPError, PluginError
from bottle import default_app, request, template as _template
from collections import Iterable
from inspect import getargspec


class InjectPlugin(object):
    api = 2

    def __init__(self, keyword, value):
        self.name = keyword
        self.keyword = keyword
        self.value = value

    def setup(self, app):
        for other in app.plugins:
            if hasattr(other, 'keyword') and self.keyword == other.keyword:
                raise PluginError('Found another plugin (%s:%s)' % (other.name, other.keyword) +
                                  ' with conflicting settings (non-unique keyword).')

    def apply(self, callback, context):
        args = getargspec(context.callback).args
        if self.keyword not in args:
            return callback

        def wrapper(*args, **kwargs):
            kwargs[self.keyword] = self.value
            return callback(*args, **kwargs)

        return wrapper


def exception_logger(func):
    def wrapper(*args, **kargs):
        try:
            return func(*args, **kargs)
        except Exception, e:
            if not isinstance(e, HTTPResponse) or isinstance(e, HTTPError):
                logging.exception('Application raise an exception')
            raise
    return wrapper


def subapps(app=None):
    if app is None:
        app = default_app()

    save = set()
    for route in app.routes:
        target = route.config.get('mountpoint.target')
        if target is not None and target not in save:
            save.add(target)
            yield target


def _install(plugin, app):
    app.install(plugin)
    for subapp in subapps(app):
        subapp.install(plugin)


def install(plugin, app=None):
    if app is None:
        app = default_app()

    if isinstance(plugin, Iterable):
        for plug in plugin:
            _install(plug, app)

    else:
        _install(plugin, app)


def urlfor(url):
    return request.script_name + url


def template_urlfor(url):
    return 'template' + urlfor(url)


def template(tpl, callback=template_urlfor, **kargs):
    return _template(callback(tpl), **kargs)
