#!/usr/bin/python
from optparse import OptionParser
import swarmtoolscore
import sys
import httplib
import os

def usage(script_name):
    print "%s [consume] \n"%(script_name)
    print "Use '%s [method] --help' for a method's usage and options."%(script_name)
    sys.exit()

def consume(api_key, args):
    if len(args) != 2:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    swarm_id = args[1]
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("GET", "/stream?swarm_id=%s"%(swarm_id), None, {"x-bugswarmapikey":api_key, "connection":"keep-alive"})
    resp = conn.getresponse()
    while(1):
        txt = resp.read(1)
        sys.stdout.write(txt)
    conn.close();

def main():
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    if sys.argv[1] == "consume":
        opt_usage = "usage: %s <swarm_id>"%(sys.argv[1])
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        consume(keys["consumer"], args)

main()
