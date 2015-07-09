#!/usr/bin/python
# -*- coding: utf-8 -*-
import hashlib
import logging
import sys


def app_init(debug=False):
    reload(sys).setdefaultencoding("utf-8")

    if debug:
        logging.basicConfig(level=logging.DEBUG)


def sha1(string):
    return hashlib.sha1(string).hexdigest().upper()
