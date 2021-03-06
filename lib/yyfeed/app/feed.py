#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import Bottle, abort, default_app, request, response, route

from ..db import Feed, FeedItem
from ..feed import Atom1Feed

__all__ = ['app']

app = Bottle()
with app:
    assert app is default_app()

    ITEM_MAX_NUM = 100


    @route('/')
    @route('/<id>')
    def feed(db, id='default'):
        feed = db.query(Feed).get(id)
        if feed is None:
            abort(404, 'No such feed [%s].' % id)

        atom = Atom1Feed(
            id=request.url,
            title=feed.title,
            link=feed.link,
            description=feed.description,
        )

        for feedItem in (
                db.query(FeedItem)
                        .filter_by(feed_id=id)
                        .filter(FeedItem.description != None)
                        .order_by(FeedItem.datetime.desc(), FeedItem.id.desc())
                        .limit(ITEM_MAX_NUM)
        ):
            if feedItem.datetime:
                atom.add_item(
                    title=feedItem.title,
                    link=feedItem.link,
                    description=feedItem.description,
                    unique_id=feedItem.id,
                    pubdate=feedItem.datetime,
                )
            else:
                atom.add_item(
                    title=feedItem.title,
                    link=feedItem.link,
                    description=feedItem.description,
                    unique_id=feedItem.id,
                )

        response.headers['Content-Type'] = atom.mime_type + '; charset=UTF-8'
        return atom.writeString('utf-8')
