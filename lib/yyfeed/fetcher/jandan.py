#!/usr/bin/python
# -*- utf-8 -*-

from os import environ

from ..util.url import urlsoup, soup_filter


def _urlsoup(url, **kargs):
    environ['disable_fetchurl'] = 1
    soup = urlsoup(url, **kargs)
    environ['disable_fetchurl'] = 0
    return soup


class Jandan(object):
    baseUrl = "http://jandan.net/ooxx"

    _filter = soup_filter('ol', 'commentlist')


    def __init__(self, id='default'):
        self.id = id

        if 'SERVER_SOFTWARE' in environ:
            self._urlsoup = _urlsoup
        else:
            self._urlsoup = urlsoup


    def fetch(self, page=None):
        url = self.baseUrl
        if page:
            url = "%s/page-%d" % (url, page)

        soup = self._urlsoup(url, parse_only=self._filter)

        ret = []
        for item in soup.find_all('li'):
            if not item.get('id'):
                continue

            text = item.find('div', 'text')
            a = text.find('span', 'righttext').a

            imgs = []
            for img in text.find_all('img'):
                imgs.append('<p><img src="%s"/></p>' % img.get('org_src', img.get('src')))

            entry = {
                'id': item['id'],
                'title': a.text,
                'link': a['href'],
                'description': '\n'.join(imgs),
            }

            ret.append(entry)

        return ret
