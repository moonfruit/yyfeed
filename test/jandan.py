#!/usr/bin/python
# -*- utf-8 -*-

from yyfeed.fetcher.jandan import Jandan


def main():
    for item in Jandan().fetch():
        print('--------')
        print(item)


if __name__ == '__main__':
    main()
