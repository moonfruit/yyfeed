#!/usr/bin/python
# -*- utf-8 -*-

from yyfeed.fetcher.iplaymtg import IPlayMtg


def main():
    fetcher = IPlayMtg()
    first = None
    for item in fetcher.fetch(1):
        if not first:
            first = item
        print('--------')
        print(item)
    print('--------')
    print(fetcher.fetch_item(first['link']))


if __name__ == '__main__':
    main()
