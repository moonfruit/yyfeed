#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from re import match, sub
from urllib import quote

from ..util.url import urlsoup, soup_filter


class IPlayMtg(object):
    domain = "http://www.iplaymtg.com"
    baseUrl = domain + "/read/hs"

    _menu_filter = soup_filter('div', 'imn_a')
    _item_filter = soup_filter('div', 'mn_view_1')


    def __init__(self, id='default', cache=None):
        self.id = id
        self.cache = cache


    def fetch(self, page=None):
        url = self.baseUrl
        if page:
            url = "%s/index.php?page=%d" % (url, page)

        soup = urlsoup(url, parse_only=self._menu_filter)

        ret = []
        for item in soup.find_all('div', 'imn_loop_c'):
            title = item.find('p', 'p1').a
            link = title['href']

            dt = item.find('span', 's1').text
            dt = match(r'(\d+)-(\d+)-(\d+) +(\d+):(\d+)', dt)
            dt = (int(e) for e in dt.groups())
            dt = datetime(*dt)

            entry = {
                'id': sub(r'article-(.+)-1\.html', r'\1', link),
                'title': title.text,
                'link': '%s/%s' % (self.domain, link),
                # 'description': self.fetch_item(link),
                'datetime': dt,
            }

            ret.append(entry)

        return ret


    def fetch_item(self, url):
        soup = urlsoup(url, parse_only=self._item_filter)
        table = soup.find('table', 'vwtb')

        for img in table.find_all('img'):
            img2 = soup.new_tag('img')
            if img['src'].startswith('http'):
                img2['src'] = img['src']
            else:
                img2['src'] = '%s/%s' % (self.domain, img['src'])
            img.replace_with(img2)

        for a in table.find_all('a'):
            href = a['href']
            if not href or href == 'javascript:;':
                a.unwrap()
            elif not href.startswith('http'):
                a['href'] = '%s/%s' % (self.domain, href)
            elif href.startswith('http://www.iplaymtg.com/card/hs'):
                a.string.wrap(soup.new_tag('b'))
                a.unwrap()

        return str(table)
