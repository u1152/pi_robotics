#!/usr/bin/env python2
# -*- coding: utf-8 -*-

__author__ = 'Elia_Reshetov'
__version__ = '1.0'

import logging

main = dict(
    VERSION = __version__,
    AUTHOR = __author__,
    ABOUT = '',
)

server = dict(
    BUFSIZE = 1024,    # reasonably sized buffer for data
    MAX_CONNECTIONS = 11,   # maximum number of queued connections we'll allow
    PROTOCOL = 'TCP',    # can be ['TCP', 'UDP']
    VERSION = __version__,
)

logging = dict(
    logfile   = "start_server.log",
    infosplit = ' : ',
    logformat = '%(asctime)-6s: %(levelname)-8s : %(message)s',
    strftime  = '%d.%m.%Y %H:%M:%S',
    loglevel  = logging.DEBUG,
)

robot_api = dict(
	pwm_tl_pin = 7,
	pwm_tr_pin = 2,
	pwm_bl_pin = 0,
	pwm_br_pin = 3,
	
	dir_tl_pin = 1,
	dir_tr_pin = 4,
	dir_bl_pin = 5,
	dir_br_pin = 6,

	turret_steps = 8,
        turret_dir = 9,
    pwm_range = 100,
)

if __name__ == '__main__':
    print "This is python module '{}'".format(__file__)
