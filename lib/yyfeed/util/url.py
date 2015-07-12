#!/usr/bin/python
# -*- coding: utf-8 -*-
from urlparse import urlparse

from bs4 import BeautifulSoup, SoupStrainer
from urllib import urlencode
from urllib2 import build_opener, HTTPCookieProcessor


_opener = build_opener(HTTPCookieProcessor())
_opener.addheaders = [('User-agent', 'Mozilla/5.0')]


def urlget(url, data=None, **kargs):
    if urlparse(url).scheme == '':
        return open(url)

    if data is None:
        data = kargs
    elif isinstance(data, dict):
        data.update(kargs)
    else:
        kargs['data'] = data
        data = kargs

    return _opener.open(url, data and urlencode(data) or None)


def urlsoup(url, **kargs):
    return BeautifulSoup(urlget(url), 'lxml', **kargs)


def soup_filter(*args, **kargs):
    return SoupStrainer(*args, **kargs)
