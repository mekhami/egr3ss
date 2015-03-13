#!/usr/bin/python

import threading
import time
import SocketServer
import sys
import argparse
import logging
from utils import info, warn, good

#############################################################################
# A fork of egress_lister.py by Dave Kennedy (ReL1K). http://bit.ly/1DLpEwV #
#############################################################################

# Todo:
#
# Consider threaded HTTP servers instead of TCP

# Nmap port parsing from: https://python-portscanner.googlecode.com/svn/trunk/nmap.py
# Threaded TCP handling from: https://www.trustedsec.com/february-2012/new-tool-release-egress-buster-find-outbound-ports/

print """
-[ egr3ss.py | by @_wald0 | v0.2
-[ Based on egress_listener.py by Dave Kennedy
-[ See http://bit.ly/1dLpEwV for info
"""

# Grab our argument values with ArgParse
parser = argparse.ArgumentParser(description='Stand up TCP servers for reverse TCP port scanning')
parser.add_argument('-p', '--ports', help='The ports to listen on', action='store')
parser.add_argument('-i', '--ipaddr', help='The IP address your victim will go to', action='store')
parser.add_argument('-l', '--logfile', help='The file to output log data to', action='store')
#parser.add_argument('-v', '--verbose', help='Show verbose output', action='store')

args = parser.parse_args()
myIP = args.ipaddr
myLOG = args.logfile

# Set up the logger
logging.basicConfig(
        filename=myLOG,
        level=logging.DEBUG,
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )
logging.info("Starting log.")

# Nmap-style port parsing from: https://python-portscanner.googlecode.com/svn/trunk/nmap.py
ranges = (x.split("-") for x in args.ports.split(","))
ports = [i for r in ranges for i in range(int(r[0]), int(r[-1]) + 1)]

# From Dave Kennedy's egress_listener.py:
# base class handler for socket server
class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    # handle the packet
    def handle(self):
        self.data = self.request.recv(1024).strip()
        good("%s connected on port: %s" % (self.client_address[0], self.server.server_address[1]))
        logging.info("%s %s" % (self.client_address[0],self.server.server_address[1]))

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":

    for port in ports:
        socketserver = ThreadedTCPServer(('', port), ThreadedTCPRequestHandler)
        socketserver_thread = threading.Thread(target=socketserver.serve_forever)
        socketserver_thread.setDaemon(True)
        socketserver_thread.start()
        info("Listening on port: " + str(port))
        logging.info("Listening on port " + str(port))

    for port in ports:
        html_str = '<img src=http://' + str(myIP) + ':' + str(port) + '/check.png><br>\n'
        with open("egr3ss.html", "a+") as html_file:
            html_file.write(html_str)

        info("HTML written to egr3ss.html")
        warn("Put that HTML into your web root's index.html")
        warn("Trick your victim into visiting http://" + myIP + "/")
        warn("Ctrl+C to exit")

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print "\n"
            info("Exiting. Run egr3ss-report.py for a nicely formatted log report.")
            logging.info("Ending log")
            break
