#!/usr/bin/env python2
# -*- coding: utf-8 -*-

__author__ = 'Elia_Reshetov'
__version__ = '1.0'

import socket
import logging

logger = logging.getLogger('')

class TCPClient(object):
    """Base client class"""
    
    def __init__(self,
                 host,
                 port,
                 RequestHandlerClass):
        self.host = host
        self.port = port
        self.RequestHandlerClass = RequestHandlerClass
        self.socket = None

    def connect(self, ):
        """Connect to server

        Returns:
            connection object
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            logger.info('Try connect to {}:{}'.format(self.host,
                                                         self.port))
            self.socket.connect((self.host, self.port))
            logger.info('Connection established to {}:{}, {}'.format(
                self.host,
                self.port,
                self.socket))
        except socket.error as err:
            logger.error("Can't connect to {}:{}, {}".format(self.host,
                                                             self.port,
                                                             err))
            self.RequestHandlerClass.handle_error(err)
            return

        try:
            self.RequestHandlerClass.handle_connection(self.socket,
                                                       self.host,
                                                       self.port)
        finally:
            self.socket.close()
            logger.info('Connection close for {}:{}, {}'.format(self.host,
                                                                self.port,
                                                                self.socket))


    def send(self, data):
        """Send a data string to the socket.
        Return the number of bytes sent;
        this may be less than len(data) if the network is busy
        """
        sent = self.socket.send(data)
        if sent < len(data):
            self.RequestHandlerClass.handle_error()
        print 'send', sent, len(data)

    def recv(self, buf_size=1024):
        """Receive up to buffersize bytes from the socket.
        When no data is available, block until at least one byte is available
        or until the remote end is closed.
        When the remote end is closed
        and all data is read, return the empty string.
        """
        recieved = self.socket.recv(buf_size)
        print 'recieved', recieved

    def close(self):
        """Close connection"""
        self.socket.close()
        logger.info('Connection closed {}:{}'.format(self.host,
                                                     self.port))

class BaseRequestHandler(object):

    def handle_connection(self, connection, host, port):
        pass

    def handle_error(self, exception):
        pass

#    def handle_connection(self, connection, client_addr):
#        pass

if __name__ == '__main__':
    print "This is python module '{}'".format(__file__)
