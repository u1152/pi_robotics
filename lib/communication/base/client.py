__author__ = 'Danse Macabre'

import logging

class Client(object):

    logger = logging.getLogger('')

    def __init__(self):
        pass

class RequestHandler(object):

    def handle_connection(self, connection, host, port):
        pass

    def handle_error(self, exception):
        pass

#    def handle_connection(self, connection, client_addr):
#        pass
