#!/usr/bin/env python
# -*- coding: utf-8 -*-

from re import sub

from bottle import Bottle, default_app, route

from ..db import Feed, FeedItem


__all__ = ['app']


app = Bottle()
with app:
    assert app is default_app()

    jandan_id = 'default'

    @route('/')
    @route('/default')
    @route('/jandan')
    def jandan(db, jandan):
        feed = db.query(Feed).get(jandan_id)
        if feed is None:
            feed = Feed(
                id = jandan_id,
                title = '煎蛋妹子图',
                link = 'http://jandan.net/ooxx',
                description = '煎蛋妹子图 Feed 生成器',
                data = {'lastPage': 900}
            )
            db.add(feed)

        page, content = _jandan_fetch(db, jandan)

        lastPage = feed.data['lastPage']
        if lastPage != page:
            page, content2 = _jandan_fetch(db, jandan, lastPage)
            content += "\n" + content2
            feed.data = feed.data.copy()
            feed.data['lastPage'] = lastPage + 1
            db.merge(feed)

        return content


def _jandan_fetch(db, jandan, page=None):
    content = ''
    for item in jandan.fetch(page):
        if not page:
            page = int(sub(r'.*page-([0-9]+).*', r'\1', item['link']))

        content += item['description']

        feedItem = FeedItem(**item)
        feedItem.feed_id = jandan.id
        db.merge(feedItem)

    return page, content
