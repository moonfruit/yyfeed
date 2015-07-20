#!/usr/bin/python
# -*- coding: utf-8 -*-
from logging import error
from urlparse import urlparse

from bs4 import BeautifulSoup, SoupStrainer
from urllib import urlencode
from urllib2 import build_opener, Request, BaseHandler, HTTPCookieProcessor


HTTP_HEADER = {'User-agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'}


class HttpProcessor(BaseHandler):
    handler_order = 499

    def http_open(self, req):
        error("req.headers = %s", req.headers)
        error("req.un_headers = %s", req.unredirected_hdrs)
        return None

    def http_response(self, req, rsp):
        error("rsp.headers = %s", rsp.headers)
        return rsp

    def http_error_403(self, req, fp, code, msg, hdrs):
        return fp


_opener = build_opener(HTTPCookieProcessor())


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

    req = Request(url, headers=HTTP_HEADER)
    if data:
        req.add_data(urlencode(data))

    return _opener.open(req)


def urlsoup(url, data=None, **kargs):
    return BeautifulSoup(urlget(url, data), 'lxml', **kargs)


def soup_filter(*args, **kargs):
    return SoupStrainer(*args, **kargs)
