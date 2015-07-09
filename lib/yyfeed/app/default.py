#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import Bottle, default_app, route


__all__ = ['app']


app = Bottle()
with app:
    assert app is default_app()

    @route('/')
    def login():
        return 'Hello, World!'
