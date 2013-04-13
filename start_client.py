#!/usr/bin/env python2
# -*- coding: utf-8 -*-

__author__ = 'Elia_Reshetov'
__version__ = '1.0'

import sys
import argparse
import logging

from client import TCPClient, BaseRequestHandler

from client_settings import client as client_settings,\
    logging as log_settings

settings = dict(client_settings) # copy server_settings
logger = logging.getLogger('')

def parse_args():
    """
    Returns:
        ArgumentParser object
    """

    parser = argparse.ArgumentParser(
        add_help=True,
        prefix_chars='-',
        version = client_settings['VERSION'],
        description='Python socket server')
    parser.add_argument('host',
                        type=str,
                        help='Host addr')
    parser.add_argument('port',
                        type=int,
                        help='Lesten port')
    parser.add_argument('--bufsize',
                        type=int,
                        default=settings['BUFSIZE'],
                        help='Reasonably sized buffer for data')
    parser.add_argument('--protocol',
                        type=str,
                        default=settings['PROTOCOL'],
                        choices=['TCP', 'UDP'],
                        help="Used transport protocol")
    parser.add_argument('--debug', '-d',
                        default=False,
                        help="Debug mode",
                        action="store_true")

    params = parser.parse_args()
    settings['HOST'] = params.host
    settings['PORT'] = params.port
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

class ClientHandler(BaseRequestHandler):

    def handle_connection(self, connection, host, port):
        data = ' '
        while data:
            data = raw_input('send to {}:{} >> '.format(host, port))
            send = connection.send(data)
            if len(data) < send:
                print "Send {} bytes instead {}".format(send, len(data))
            answer = connection.recv(1024)
            print 'Server answer:', answer
        connection.close()

    def handle_error(self, exception):
        pass

def main(argv=None):
    if argv is None:
        argv = sys.argv
    params = parse_args()
    print params
    config_logging()

    handler = ClientHandler()
    if params.protocol == 'TCP':
        ClientClass = TCPClient
#    elif params.protocol == 'UDP':
#        server_class = UDPServer
    client = ClientClass(settings['HOST'],
                         settings['PORT'],
                         handler)
    client.connect()

if __name__ == '__main__':
    main()
