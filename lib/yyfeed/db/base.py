#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.attributes import InstrumentedAttribute


ID_SIZE = 64
DESC_SIZE = 4000


class Base(object):

    def __str__(self):
        return self._to_str()

    def __repr__(self):
        return self._to_str(repr)

    def _to_str(self, callback=str):
        attrs = []
        for attr in dir(self.__class__):
            if (attr.startswith('_') or attr == 'metadata'):
                continue

            if isinstance(getattr(self.__class__, attr), InstrumentedAttribute):
                value = getattr(self, attr)
                if value is not None:
                    attrs.append('%s=%s' % (attr, callback(value)))

        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))


Base = declarative_base(cls=Base)
