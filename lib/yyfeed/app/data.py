#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from bottle import Bottle, default_app, request, route

from ..db import FeedItem

__all__ = ['app']

app = Bottle()
with app:
    assert app is default_app()

    ITEM_MAX_NUM = 30


    @route('/')
    @route('/images')
    def feed(db):
        offset = request.params.get('offset')
        if offset:
            offset = int(offset)
        else:
            offset = 0

        limit = request.params.get('limit')
        if limit:
            limit = int(limit)
        else:
            limit = ITEM_MAX_NUM

        if offset < 0:
            offset = 0

        if limit < 1:
            limit = 1
        elif limit > ITEM_MAX_NUM:
            limit = ITEM_MAX_NUM

        imgs = []
        for feedItem in (
                db.query(FeedItem)
                        .filter(FeedItem.feed_id.in_(('default', 'ttrss')))
                        .filter(FeedItem.description != None)
                        .order_by(FeedItem.datetime.desc(), FeedItem.id.desc())
                [offset:limit]
        ):
            desc = re.sub(r'^.*src="(.*)".*$', r'\1', feedItem.description, flags=re.M)
            imgs.extend(desc.split('\n'))
        return {"imgs": imgs}
