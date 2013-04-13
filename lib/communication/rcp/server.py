import struct
import threading

from lib.communication.tcp.server import Server as TcpServer
from lib.communication.base.server import RequestHandler as TcpRequestHandler
from lib.robot.base import Robot

class Server(TcpServer):

    def __init__(self, host, port, robot):
        TcpServer.__init__(
            self,
            host,
            port,
            RequestHandler(robot),
            activate=True
        )

class RequestHandler(TcpRequestHandler):

    def __init__(self, robot):
        self.robot = robot

    def handle_connection(self, connection, client_address):
        threading.Thread(target=self.__process_commands, args=(connection))
        threading.Thread(target=self.__process_sensors, args=(connection))

    def handle_error(self, exception):
        self.robot.stop()

    def __process_commands(self, connection):
        while True:
            try:
                code = ord(connection.recv(1))
            except KeyError:
                'Unknown command code: {}'.format(code)
            cmd = Command(*self.robot.api[code])
            args = struct.unpack(cmd.fmt, connection.recv(cmd.size))
            getattr(self.robot, cmd.name)(*args)

    def __process_sensors(self, connection):
        pass

class Command:

    def __init__(self, name, fmt):
        self.name = name
        self.fmt = fmt

    @property
    def size(self):
        return struct.calcsize(self.fmt)
