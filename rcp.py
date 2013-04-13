#!/usr/bin/env python2
# -*- coding: utf-8 -*-

__author__ = 'Elia_Reshetov'
__version__ = '1.0'
__info__ = 'Robot Command Protocol'

# PWM_freq = 10'000 / RANGE
# command format = [
#               direction_left:byte = {'f', 'b'},
#               direction_right:byte = {'f', 'b'},
#               mark_PWM0:uint,
#               mark_PWM1:uint,
# ]

TRANSACTION_SIZE = 10 # bytes

class Server(object):
    """Client-side class to provide communication functions"""

#    @staticmethod
#    def handshake(cls, connection, host, port):
#        """Handshake with server"""
#        pass

    @staticmethod
    def parse_data(data):
        """Parse data with format command_format"""

        return dict(
            direction_left = data[0],
            direction_right = data[1],
            mark_PWM_left = data[2:5],
            mark_PWM_right = data[6:9],
        )

    @staticmethod
    def send_fault(connection, desc=''):
        connection.send('error {}'.format(desc))

    @staticmethod
    def send_ok(connection):
        connection.send('OK')

if __name__ == '__main__':
    print "This is python module '{}'".format(__file__)
