__author__ = 'Danse Macabre'

class Robot:

    class API:

        def __init__(self):
            self.commands = dict()
            self.sensors = dict()

    def __init__(self, debug):
        self.debug = debug
        self.api = Robot.API()

    def stop(self):
        pass
