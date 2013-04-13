#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from lib.communication import tcp

__author__ = 'Elia_Reshetov'
__version__ = '1.0'

import socket


class Server(tcp.Server):
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