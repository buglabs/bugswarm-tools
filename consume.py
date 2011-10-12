#!/usr/bin/python
from optparse import OptionParser
from lib import swarmtoolscore
import sys
import httplib
import os

def usage(script_name):
    print "%s [consume] \n"%(script_name)
    print "Use '%s [method] --help' for a method's usage and options."%(script_name)
    sys.exit()

def consume(hostname, api_key, swarm_id, resource_id):
    conn = httplib.HTTPConnection(hostname)
    conn.request("GET", "/stream?swarm_id=%s&resource_id=%s"%(swarm_id, resource_id), None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    while(1):
        txt = resp.read(1)
        sys.stdout.write(txt)
        sys.stdout.flush()
    conn.close();

def main():
    server_info = swarmtoolscore.get_server_info()
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    elif sys.argv[1] == "consume":
        opt_usage = "usage: \n  %s SWARM_ID RESOURCE_ID"%(sys.argv[1])
        opt_usage += "\n\n  *SWARM_ID: The ID of the swarm to consume." \
                    +"\n  *RESOURCE_ID: The ID of the resource to use for consumption."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        if len(args) != 3:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        swarm_id = args[1]
        resource_id = args[2]
        consume(server_info["hostname"], keys["participation"], swarm_id, resource_id)
    else:
        usage(sys.argv[0])
main()
