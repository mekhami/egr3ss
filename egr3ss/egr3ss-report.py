import os
import argparse
import re
import sys
import urllib

# Print banner
print """
-[ egr3ss-report.py | by @_wald0 | v0.2
"""

# Define our color notifcations
class bcolors:
        WARN = '\033[93m\033[1m[!] \033[0m'
        GOOD = '\033[92m\033[1m[+] \033[0m'
        INFO = '\033[94m\033[1m[*] \033[0m'

# Configure our parser and grab parser arguments
parser = argparse.ArgumentParser(description='Standalone log parser for egr3ss.py')
parser.add_argument('-l', '--logfile', help='The log file to parse', action='store')
args = parser.parse_args()
logFile = args.logfile

# "r" will match regular expression for an IP address (but will
# also match things like 999.123.666.000)
r = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

# Check if we have already associated a port with a given IP
def portcheck(port, portlist):
    for p in portlist:
        if p == port:
            return 'True'
    return  'False'

# Check if we already have an entry for the IP
def ipcheck(ip,port):
    i=0
    for key in ips:
        if key['ip']:
            if portcheck(port, key['port']) == 'False':
                return ('True', i)
        i += 1
    return ('False', i)

# Analyze the specified log file
with open(logFile) as f:
    print bcolors.INFO + "Analying " + logFile
    lines = f.readlines()
    ips = {}
    for line in lines:
        line = line.rstrip('\n')
        if r.search(line):
            ip = str(line.split(" ")[-2:-1]).strip("[]'")
            port = str(line.split(" ")[-1:]).strip("[]'")
            if ip in ips:
                pass
            else:
                ips[ip] = []
            if port in ips[ip]:
                pass
            else: ips[ip].append(port)

# Geolocation
ip_country={}
ip_city={}
for host in ips:
    try:
        response = urllib.urlopen('http://api.hostip.info/get_html.php?ip=' + host + '&position=true').readlines()
        for line in response:
            if 'Country:' in line:
                ip_country[host]=line.split(':')[1].strip('\n')
            if 'City:' in line:
                ip_city[host]=line.split(':')[1].strip('\n')
    except:
        ip_country[host] = ""
        ip_city[host] = ""
        print bcolors.WARN + "Error: could not retrive geo IP information from hostip.info for " + host

# Print output to the console
for host in ips:
    port_or_ports='port'
    if len(ips[host]) > 1:
        port_or_ports='ports'
    print (bcolors.GOOD
    + host
    + ' connected on '
    + port_or_ports
    + ' '
    + ','.join(map(str, ips[host]))
    + ' -'
    + ip_city[host]
    + '  '
    + ip_country[host]
    )
