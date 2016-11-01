#Omnet-Interface.py

import os
import sys
import tempfile
import shutil
import socket
import struct
import subprocess
import time
import signal
import exceptions
import thread
import xml.dom.minidom
import select
import logging
import atexit
from optparse import OptionParser


def main():
    print ("in main loop")
    parser = OptionParser()
    parser.add_option("-H", "--host", dest="host", default="localhost", help="specify the host ip of omnet [default: %default]", metavar="HOST")
    parser.add_option("-p", "--port", dest="port", default="9998", help="specify the host port of omnet [default: %default]", metavar="PORT")
    (options, args) = parser.parse_args()

    if args:
        logging.warning("Superfluous command line arguments: \"%s\"" % " ".join(args))

    print("Attempting to establish a connection to %s:%s" % (options.host, options.port))

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((options.host, int(options.port)))
    listener.listen(5)
    logging.info("Listening on port %s" % options.port)
    try:
        while True:
            conn, addr = listener.accept()
            logging.debug("Connection from %s on port %d" % addr)
            print("Received following communication:%s" % conn)

    except exceptions.SystemExit:
        logging.warning("Killed.")

    except exceptions.KeyboardInterrupt:
        logging.warning("Keyboard interrupt.")

if __name__ == '__main__':
    main()
