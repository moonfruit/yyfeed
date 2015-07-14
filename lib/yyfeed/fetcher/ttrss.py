#!/usr/bin/python
# -*- utf-8 -*-

from datetime import datetime
from re import sub

from ..util.url import urlsoup, soup_filter


class Ttrss(object):
    baseUrl = "http://ttrss.com"

    _menu_filter = soup_filter('ul', id='post_container')
    _item_filter = soup_filter('div', id='post_content')


    def __init__(self, id='default', cache=None):
        self.id = id
        self.cache = cache


    def fetch(self, page=None):
        url = self.baseUrl
        if page:
            url = "%s/page/%d" % (url, page)

        soup = urlsoup(url, parse_only=self._menu_filter)

        ret = []
        for item in soup.find_all('li'):
            h2 = item.h2
            link = h2.a['href']

            dt = item.find('span', class_='info_date').text
            dt = datetime(datetime.today().year, int(dt[:2]), int(dt[3:5]))

            entry = {
                'id': sub(r'.*\/(\d*)\.html', r'\1', link),
                'title': h2.text,
                'link': link,
                # 'description': self.fetch_item(link),
                'datetime': dt,
            }

            ret.append(entry)

        return ret


    def fetch_item(self, url):
        soup = urlsoup(url, parse_only=self._item_filter)

        ret = []
        for item in soup.find_all('img'):
            ret.append('<p>%s</p>' % item)

        return '\n'.join(ret)
