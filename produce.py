#!/usr/bin/python
from optparse import OptionParser
import swarmtoolscore
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

def produce(api_key, args):
    if len(args) != 4:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    swarm_id = args[1]
    resource_id = args[2]
    feed_name = args[3]
    global conn 
    conn = httplib.HTTPConnection('api.bugswarm.net')
    sel = "/resources/%s/feeds/%s?swarm_id=%s"%(resource_id, feed_name, swarm_id)
    print sel
    print api_key
    conn.putrequest("PUT", sel)
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
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    signal.signal(signal.SIGINT, signal_handler)
    if sys.argv[1] == "produce":
        opt_usage = "usage: <data> | python %s <swarm_id> <resource_id> <feed_name>"%(sys.argv[1])
        opt_usage += "\n*data: The data to produce in the Feed. Valid forms; \"echo 'data here'\", \"cat <filename>\"." \
                    +"\n*swarm_id: The ID of the Swarm to produce to. This is a really long, unique identifier." \
                    +"\n*resource_id: The ID of the Resource to produce with. This is the \"id\" field in the resource's listed JSON." \
                    +"\n*feed_name: The name of the Feed you are producing."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        produce(keys["producer"], args)

main()
