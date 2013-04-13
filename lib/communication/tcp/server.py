from lib.communication import base

import socket

class Server(base.Server):
    socket_type = socket.SOCK_STREAM

    def __init__(self, *args, **kwargs):
        """Constructor.  May be extended, do not override."""
        base.Server.__init__(self, *args, **kwargs)
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
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        # self.server_address = self.socket.getsockname()

    def activate(self):
        """Called by constructor to activate the server.

        May be overridden.

        """
        self.socket.listen(self.max_connections)
        self.logger.info('Server is running at rcp://{}:{}'.format(self.host,
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
            self.logger.error("Error '{}' in shutdown_connection, {}".format(
                err, connection))
        self.close_connection(connection)

    def close_connection(self, connection):
        """Called to clean up an individual request."""
        connection.close()
        self.logger.info('Connection {} closed'.format(connection))
