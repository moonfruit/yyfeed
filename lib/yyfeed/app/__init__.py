#!/usr/bin/env python
# -*- coding: utf-8 -*-
assert __name__ is not '__main__'

from importlib import import_module

from bottle import mount, redirect, route, static_file


def _mount(name):
    mount(name, import_module('.' + name, __name__).app)
_mount('feed')
_mount('fetcher')


@route('/')
def home():
    redirect('/feed')


# noinspection PyUnresolvedReferences
@route('/favicon.ico')
@route('/static/<filepath:path>')
def server_static(filepath='favicon.ico'):
    return static_file(filepath, root='static')
