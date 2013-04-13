#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import threading

__author__ = 'Elia_Reshetov'
__version__ = '1.0'

import socket
import select
import logging

class Server(object):
    """Abstract Server class"""

    logger = logging.getLogger('')

    def __init__(self,
                 host,
                 port,
                 handler,
                 buffer_size=1024,
                 max_connections=1,
                 **kwargs):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.max_connections = max_connections
        self.handler = handler
        self.socket = None
        self.__is_started = False
        self.__is_shut_down = threading.Event()

    def start(self):
        """Start server"""
        self.__is_shut_down.clear()
        self.__is_started = True
        try:
            while self.__is_started:
                # logger.info('Server accept loop started/continued')
                z = [[self.socket]] * 3
                input_ready, output_ready, except_ready = select.select(
                    *z)
                print 'here!'
                if self.socket in input_ready:
                    try:
                        connection, client_address = self.wait_for_connection()
                        self.logger.info('Connected by {}, {}'.format(
                            client_address[0],
                            connection))
                    except socket.error as exception:
                        self.logger.warning('Error {} in wait_for_connection'.format(
                            exception))
                        # self.handler.handle_connection_error(exception)
                        continue
                    try:
                        self.handler.handle_connection(
                            connection,
                            client_address)
                    except Exception as exception:
                        self.logger.error("Error {}.'{}' in handle_connection, "
                                     "connection={}".format(
                            exception.__class__,
                            exception, connection))
                    finally:
                        self.shutdown_connection(connection)
        finally:
            self.__shutdown_request = False
            self.__is_shut_down.set()

    def shutdown(self):
        """Stops the serve_forever loop.

        Blocks until the loop has finished. This must be called while
        serve_forever() is running in another thread, or it will
        deadlock.
        """
        self.stop()
        self.socket.close()
        self.logger.info('Server shutdown')


    def stop(self):
        """Stop server"""
        self.__is_started = False
        self.__is_shut_down.wait()
        self.logger.info('Server listen loop stopped')

    def wait_for_connection(self):
        raise Exception('communication.base.server: Server.wait_for_connection() method must be overriden')

    def shutdown_connection(self, connection):
        """Called to shutdown and close an individual request."""
        self.close_connection(connection)

    def close_connection(self, connection):
        """Called to clean up an individual request."""
        self.logger.info('Connection {} closed'.format(connection))

class RequestHandler(object):
    def handle_connection_error(self):
        pass

    def handle_error(self, exception):
        pass

    def handle_connection(self, connection, client_address):
        pass
