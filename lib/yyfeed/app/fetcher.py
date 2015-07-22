#!/usr/bin/env python
# -*- coding: utf-8 -*-

from re import sub

from bottle import Bottle, default_app, redirect, request, route

from ..db import Feed, FeedItem
from ..util.web import urlfor


__all__ = ['app']


app = Bottle()
with app:
    assert app is default_app()

    JANDAN_PAGE_START = 900
    TTRSS_PAGE_START = 1
    IPLAYMTG_PAGE_START = 1


    @route('/')
    @route('/default')
    @route('/jandan')
    def jandan(db, jandan):
        page = request.params.get('page')
        if page:
            page = int(page)
            if page < JANDAN_PAGE_START:
                page = JANDAN_PAGE_START

        feed = db.query(Feed).get(jandan.id)
        if feed is None:
            feed = Feed(
                id = jandan.id,
                title = '煎蛋妹子图',
                link = jandan.baseUrl,
                description = '煎蛋妹子图 Feed 生成器',
                data = {'lastPage': JANDAN_PAGE_START},
            )
            db.add(feed)

        page, content = _jandan_fetch(db, jandan, page)

        lastPage = feed.data['lastPage']
        if lastPage < page:
            page, content2 = _jandan_fetch(db, jandan, lastPage)
            content += "\n" + content2
            feed.data = feed.data.copy()
            feed.data['lastPage'] = lastPage + 1
            db.merge(feed)

        return content


    @route('/ttrss')
    def ttrss(db, ttrss):
        page = request.params.get('page')
        if page:
            page = int(page)
            if page < TTRSS_PAGE_START:
                page = TTRSS_PAGE_START

        feed = db.query(Feed).get(ttrss.id)
        if feed is None:
            feed = Feed(
                id = ttrss.id,
                title = '图图',
                link = ttrss.baseUrl,
                description = '图图 Feed 生成器',
            )
            db.add(feed)

        for item in ttrss.fetch(page):
            feedItem = FeedItem(**item)
            feedItem.feed_id = ttrss.id
            db.merge(feedItem)

        redirect(urlfor('ttrss/item'))


    @route('/ttrss/item')
    def ttrss_item(db, ttrss):
        item = (
            db.query(FeedItem)
                .filter_by(feed_id=ttrss.id)
                .filter(FeedItem.description == None)
                .order_by(FeedItem.id)
                .first()
        )

        if not item:
            return 'No item'

        item.description = ttrss.fetch_item(item.link)
        db.merge(item)

        return item.description


    @route('/iplaymtg')
    def iplaymtg(db, iplaymtg):
        page = request.params.get('page')
        if page:
            page = int(page)
            if page < IPLAYMTG_PAGE_START:
                page = IPLAYMTG_PAGE_START

        feed = db.query(Feed).get(iplaymtg.id)
        if feed is None:
            feed = Feed(
                id = iplaymtg.id,
                title = '旅法师营地 - 炉石传说',
                link = iplaymtg.baseUrl,
                description = '旅法师营地 Feed 生成器',
            )
            db.add(feed)

        for item in iplaymtg.fetch(page):
            feedItem = FeedItem(**item)
            feedItem.feed_id = iplaymtg.id
            db.merge(feedItem)

        redirect(urlfor('iplaymtg/item'))


    @route('/iplaymtg/item')
    def iplaymtg_item(db, iplaymtg):
        item = (
            db.query(FeedItem)
                .filter_by(feed_id=iplaymtg.id)
                .filter(FeedItem.description == None)
                .order_by(FeedItem.id)
                .first()
        )

        if not item:
            return 'No item'

        item.description = iplaymtg.fetch_item(item.link)
        db.merge(item)

        return item.description


def _jandan_fetch(db, jandan, page=None):
    content = ''
    for item in jandan.fetch(page):
        if not page:
            page = int(sub(r'.*page-(\d+).*', r'\1', item['link']))

        content += item['description']

        feedItem = FeedItem(**item)
        feedItem.feed_id = jandan.id
        db.merge(feedItem)

    return page, content
