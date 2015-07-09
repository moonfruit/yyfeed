#!/usr/bin/env python
# -*- coding: utf-8 -*-
assert __name__ is not '__main__'

from bottle import mount, redirect, route, static_file
from importlib import import_module


def _mount(name):
    mount(name, import_module('.' + name, __name__).app)
_mount('default')


@route('/')
def home():
    redirect('/default')


@route('/favicon.ico')
@route('/static/<filepath:path>')
def server_static(filepath='favicon.ico'):
    return static_file(filepath, root='static')
