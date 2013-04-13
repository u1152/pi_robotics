#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import threading

__author__ = 'Elia_Reshetov'
__version__ = '1.0'

import socket
import select
import logging

logger = logging.getLogger('')


class BaseServer(object):
    """Abstract Server class"""

    def __init__(self,
                 host,
                 port,
                 RequestHandlerClass,
                 buffer_size=1024,
                 max_connections=1,
                 **kwargs):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.max_connections = max_connections
        self.RequestHandlerClass = RequestHandlerClass
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
                input_ready, output_ready, except_ready = select.select(
                    *[[self.socket]] * 3)
                if self.socket in input_ready:
                    try:
                        connection, client_address = self.wait_for_connection()
                        logger.info('Connected by {}, {}'.format(
                            client_address[0],
                            connection))
                    except socket.error as exception:
                        logger.warning('Error {} in wait_for_connection'.format(
                            exception))
                        # self.RequestHandlerClass.handle_connection_error(exception)
                        continue
                    try:
                        self.RequestHandlerClass.handle_connection(
                            connection,
                            client_address)
                    except Exception as exception:
                        logger.error("Error {}.'{}' in handle_connection, "
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
        logger.info('Server shutdown')


    def stop(self):
        """Stop server"""
        self.__is_started = False
        self.__is_shut_down.wait()
        logger.info('Server listen loop stopped')

    def shutdown_connection(self, connection):
        """Called to shutdown and close an individual request."""
        self.close_connection(connection)

    def close_connection(self, connection):
        """Called to clean up an individual request."""
        logger.info('Connection {} closed'.format(connection))


class TCPServer(BaseServer):
    socket_type = socket.SOCK_STREAM

    def __init__(self, *args, **kwargs):
        """Constructor.  May be extended, do not override."""
        super(TCPServer, self).__init__(*args, **kwargs)
        self.socket = socket.socket(socket.AF_INET, self.socket_type)
        if kwargs.get('allow_reuse_address', True):
            self.allow_reuse_address = True
        if kwargs.get('activate', False):
            self.bind()
            self.activate()

    def bind(self):
        """Called by constructor to bind the socket.

        May be overridden.

        """
        if self.allow_reuse_address:
            # устанавливаем опцию повторного использования порта для того,
            # чтобы не ждать после останова сервера пока освободится порт
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        # self.server_address = self.socket.getsockname()

    def activate(self):
        """Called by constructor to activate the server.

        May be overridden.

        """
        self.socket.listen(self.max_connections)
        logger.info('Server is running at rcp://{}:{}'.format(self.host,
                                                              self.port))

    def wait_for_connection(self):
        """Get the request and client address from the socket.

        May be overridden.

        """
        return self.socket.accept()

    def shutdown_connection(self, connection):
        """Called to shutdown and close an individual request."""
        try:
            #explicitly shutdown.  socket.close() merely releases
            #the socket and waits for GC to perform the actual close.
            connection.shutdown(socket.SHUT_WR)
        except socket.error as err:
            #some platforms may raise ENOTCONN here
            logger.error("Error '{}' in shutdown_connection, {}".format(
                err, connection))
        self.close_connection(connection)

    def close_connection(self, connection):
        """Called to clean up an individual request."""
        connection.close()
        logger.info('Connection {} closed'.format(connection))


class UDPServer(TCPServer):
    """UDP server class."""

    socket_type = socket.SOCK_DGRAM

    def recieve(self):
        data, client_addr = self.socket.recvfrom(self.buffer_size)
        return (data, self.socket), client_addr

    wait_for_connection = recieve

    def activate(self):
        # No need to call listen() for UDP.
        pass

    def shutdown_connection(self, connection):
        # No need to shutdown anything.
        pass

    def close_connection(self, connection):
        # No need to close anything.
        pass


class BaseRequestHandler(object):
    def handle_connection_error(self):
        pass

    def handle_error(self, exception):
        pass

    def handle_connection(self, connection, client_address):
        pass


if __name__ == '__main__':
    print "This is python module '{}'".format(__file__)
