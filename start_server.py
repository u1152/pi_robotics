#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import Rover5

__author__ = 'Elia_Reshetov'
__version__ = '1.0'

import os
import sys
import struct
import argparse
import logging
import threading
import time
#import SocketServer

import wiringpi as wp

from server import TCPServer, BaseRequestHandler

from server_settings import main as main_settings, \
    logging as log_settings, \
    robot_api
#    server as server_settings, \

#import rcp

rover5 = Rover5.Rover5()


def parse_args():
    """
    Returns:
        ArgumentParser object
    """

    parser = argparse.ArgumentParser(
        add_help=True,
        prefix_chars='-',
        version=main_settings['VERSION'],
        description='Python socket server')
    parser.add_argument('host',
                        type=str,
                        help='Host addr')
    parser.add_argument('port',
                        type=int,
                        help='Lesten port')
    #    parser.add_argument('--bufsize',
    #                        type=int,
    #                        default=server_settings['BUFSIZE'],
    #                        help='Reasonably sized buffer for data')
    #    parser.add_argument('--max-clients',
    #                        type=int,
    #                        default=server_settings['MAX_CONNECTIONS'],
    #                        help="Maximum number of queued connections we'll allow")
    #    parser.add_argument('--protocol',
    #                        type=str,
    #                        default=server_settings['PROTOCOL'],
    #                        choices=['TCP', 'UDP'],
    #                        help="Used transport protocol")
    #    parser.add_argument('--debug', '-d',
    #                        default=False,
    #                        help="Debug mode",
    #                        action="store_true")

    params = parser.parse_args()
    return params


def config_logging():
    """
    Returns:
        logger object
    """
    formatter = logging.Formatter(log_settings['logformat'], log_settings['strftime'])
    console_logger = logging.StreamHandler()
    console_logger.setLevel(log_settings['loglevel'])
    console_logger.setFormatter(formatter)
    file_logger = logging.FileHandler(filename=log_settings['logfile'])
    file_logger.setLevel(log_settings['loglevel'])
    file_logger.setFormatter(formatter)

    logger = logging.getLogger('')
    logger.addHandler(console_logger)
    logger.addHandler(file_logger)
    logger.setLevel(log_settings['loglevel'])
    return logger

class ServerHandler(BaseRequestHandler):
#    def __init__(self):
#        super(self)
#        rover5 = Rover5.Rover5()

    def handle_connection(self, connection, client_address):
        while True:
            recieved = connection.recv(12)

            if recieved:
                print 'recv({})={}'.format(len(recieved), \
                    ' '.join(['{:X}'.format(ord(byte)) for byte in recieved])), \
                    '|', recieved

                rover5.setSpeed(int(recieved[2:5]), int(recieved[5:8]))
                rover5.setDirection(int(recieved[0]), int(recieved[1]))
                rover5.turnTurret(int(recieved[8:12]))
                connection.send('OK')
            else:
                print 'recv 0 bytes', recieved
                connection.send('error: {}'.format('recv 0 bytes'))

 
    def handle_error(self, exception):
        print 'stop!'
        self.rover5.stop()

def main(argv=None):
    if argv is None:
        argv = sys.argv
    params = parse_args()
    config_logging()
    print params

    handler = ServerHandler()
    server = TCPServer(params.host,
                       params.port,
                       handler,
                       activate=True, )
    # max_connections=params.max_clients)
    server.start()


if __name__ == '__main__':
    # os.system('cls')
    main()
