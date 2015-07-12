#!/usr/bin/python
# -*- utf-8 -*-

from yyfeed.fetcher.jandan import Jandan


def main():
    print(Jandan().fetch())


if __name__ == '__main__':
    main()
