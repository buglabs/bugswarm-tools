#!/usr/bin/python
from optparse import OptionParser
from lib import swarmtoolscore
import sys
import httplib
import os
import time
import signal

def usage(script_name):
    print "%s [produce] \n"%(script_name)
    print "Use '%s [method] --help' for a method's usage and options."%(script_name)
    sys.exit()

def signal_handler(signal, frame):
        global conn
        conn.close()
        print 'Http connection closed.'
        sys.exit(0)

def produce(hostname, api_key, swarm_id, resource_id):
    global conn 
    conn = httplib.HTTPConnection(hostname)
    sel = "/stream?swarm_id=%s&resource_id=%s"%(swarm_id, resource_id)
    print sel
    print api_key
    conn.putrequest("POST", sel)
    conn.putheader("x-bugswarmapikey", api_key)
    conn.putheader("transfer-encoding", "chunked")
    conn.endheaders()

    #Sleep required to allow the swarm server time to respond with header
    #TODO - actually wait until header is returned
    time.sleep(1)

    while True:
        try:
            msg = sys.stdin.readline()
            if (len(msg) < 1):
                break
            stripped_msg = msg.strip()
            size = hex(len(stripped_msg))[2:] + "\r\n"
            chunk = stripped_msg + "\r\n"
            conn.send(size+chunk)
            #conn.send flushes the pipe, so we need both the size and chunk to go out at the same time...
                
        except Exception as e:
            print "some sort of problem", e

    conn.send("0\r\n")
    conn.close()

def main():
    server_info = swarmtoolscore.get_server_info()
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    elif sys.argv[1] == "produce":
        signal.signal(signal.SIGINT, signal_handler)
        opt_usage = "usage: \n  DATA | python %s SWARM_ID RESOURCE_ID"%(sys.argv[1])
        opt_usage += "\n\n  *DATA: The data to produce in the Feed. Valid forms; \"echo 'data here'\", \"cat <filename>\"." \
                    +"\n  *SWARM_ID: The ID of the Swarm to produce to. This is a really long, unique identifier." \
                    +"\n  *RESOURCE_ID: The ID of the Resource to produce with. This is the \"id\" field in the resource's listed JSON."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        if len(args) != 3:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        swarm_id = args[1]
        resource_id = args[2]
        produce(server_info["hostname"], keys['master'], swarm_id, resource_id)
    else:
        usage(sys.argv[0])

main()
