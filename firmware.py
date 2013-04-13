__version__ = '1.0'

import os
import sys
import argparse
import logging

from lib.communication.rcp.server import Server as RcpServer

def parse_args():
    """
    Returns:
        ArgumentParser object
    """

    parser = argparse.ArgumentParser(
        add_help=True,
        prefix_chars='-',
        description='Python socket server'
    )
    parser.add_argument('robot',
                        type=str,
                        help='Robot class file (.py)'
    )
    parser.add_argument('host',
                        type=str,
                        help='Host addr'
    )
    parser.add_argument('port',
                        type=int,
                        help='Listen port'
    )
    #    parser.add_argument('--bufsize',
    #                        type=int,
    #                        default=server_settings['BUFSIZE'],
    #                        help='Reasonably sized buffer for data')
    #    parser.add_argument('--max-clients',
    #                        type=int,
    #                        default=server_settings['MAX_CONNECTIONS'],
    #                        help="Maximum number of queued connections we'll allow")
    #    parser.add_argument('--protocol',
    #                        type=str,
    #                        default=server_settings['PROTOCOL'],
    #                        choices=['TCP', 'UDP'],
    #                        help="Used transport protocol")
    #    parser.add_argument('--debug', '-d',
    #                        default=False,
    #                        help="Debug mode",
    #                        action="store_true")

    params = parser.parse_args()
    return params

log_settings = dict(
    logfile   = "start_server.log",
    infosplit = ' : ',
    logformat = '%(asctime)-6s: %(levelname)-8s : %(message)s',
    strftime  = '%d.%m.%Y %H:%M:%S',
    loglevel  = logging.DEBUG,
    )

def config_logging():
    """
    Returns:
        logger object
    """
    formatter = logging.Formatter(log_settings['logformat'], log_settings['strftime'])
    console_logger = logging.StreamHandler()
    console_logger.setLevel(log_settings['loglevel'])
    console_logger.setFormatter(formatter)
    file_logger = logging.FileHandler(filename=log_settings['logfile'])
    file_logger.setLevel(log_settings['loglevel'])
    file_logger.setFormatter(formatter)

    logger = logging.getLogger('')
    logger.addHandler(console_logger)
    logger.addHandler(file_logger)
    logger.setLevel(log_settings['loglevel'])
    return logger

def main(argv=None):
    if argv is None:
        argv = sys.argv
    params = parse_args()
    config_logging()
    print params

    sys.path.append(os.path.dirname(params.robot))
    exec('from %s import Robot' % os.path.basename(params.robot).rstrip('.py'))

    robot = Robot(debug=True)
    server = RcpServer(params.host, params.port, robot)

    # max_connections=params.max_clients)
    server.start()

if __name__ == '__main__':
    # os.system('cls')
    main()
