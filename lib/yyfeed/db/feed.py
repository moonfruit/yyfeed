#!/usr/bin/python
# -*- utf-8 -*-

from sqlalchemy import Column, DateTime, String, Text, ForeignKey

from .base import Base, ID_SIZE, DESC_SIZE


class Feed(Base):
    __tablename__ = 'feed'

    id = Column(String(ID_SIZE), primary_key=True)
    title = Column(String(DESC_SIZE))
    link = Column(String(DESC_SIZE))
    description = Column(String(DESC_SIZE))


class FeedItem(Base):
    __tablename__ = 'feed_item'

    feed_id = Column(String(ID_SIZE), ForeignKey("feed.id"), primary_key=True)
    id = Column(String(ID_SIZE), primary_key=True)
    title = Column(String(DESC_SIZE))
    link = Column(String(DESC_SIZE))
    # description = Column(String(DESC_SIZE))
    description = Column(Text())
    datetime = Column(DateTime())
