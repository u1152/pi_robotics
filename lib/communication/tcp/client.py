#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from lib.communication import base

__author__ = 'Elia_Reshetov'
__version__ = '1.0'

import socket


class Client(base.Client):
    """Base client class"""

    def __init__(self,
                 host,
                 port,
                 handler):
        base.Client.__init__(self)
        self.host = host
        self.port = port
        self.handler = handler
        self.socket = None

    def connect(self, ):
        """Connect to server

        Returns:
            connection object
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.logger.info('Try connect to {}:{}'.format(self.host,
                                                      self.port))
            self.socket.connect((self.host, self.port))
            self.logger.info('Connection established to {}:{}, {}'.format(
                self.host,
                self.port,
                self.socket))
        except socket.error as err:
            self.logger.error("Can't connect to {}:{}, {}".format(self.host,
                                                             self.port,
                                                             err))
            self.handler.handle_error(err)
            return

        try:
            self.handler.handle_connection(self.socket,
                                                       self.host,
                                                       self.port)
        finally:
            self.socket.close()
            self.logger.info('Connection close for {}:{}, {}'.format(self.host,
                                                                self.port,
                                                                self.socket))

    def send(self, data):
        """Send a data string to the socket.
        Return the number of bytes sent;
        this may be less than len(data) if the network is busy
        """
        sent = self.socket.send(data)
        if sent < len(data):
            self.handler.handle_error()
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
        self.logger.info('Connection closed {}:{}'.format(self.host,
                                                     self.port))