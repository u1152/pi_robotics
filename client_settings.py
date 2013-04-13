#!/usr/bin/env python2
# -*- coding: utf-8 -*-

__author__ = 'Elia_Reshetov'
__version__ = '1.0'

import logging

from server_settings import server

main = dict(
    VERSION = __version__,
    AUTHOR = __author__,
    ABOUT = '',
)

client = dict(
    BUFSIZE = server['BUFSIZE'],
    PROTOCOL = server['PROTOCOL'],
    VERSION = __version__,
)

logging = dict(
    logfile   = "client.log",
    infosplit = ' : ',
    logformat = '%(asctime)-6s: %(levelname)-8s : %(message)s',
    strftime  = '%d.%m.%Y %H:%M:%S',
    loglevel  = logging.DEBUG,
)

if __name__ == '__main__':
    print "This is python module '{}'".format(__file__)
