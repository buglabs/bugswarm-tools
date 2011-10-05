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

def produce(hostname, api_key, swarm_id, resource_id, feed_name):
    global conn 
    conn = httplib.HTTPConnection(hostname)
    sel = "/resources/%s/feeds/%s?swarm_id=%s"%(resource_id, feed_name, swarm_id)
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
    server_info = swarmtoolscore.get_server_info()
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    elif sys.argv[1] == "produce":
        signal.signal(signal.SIGINT, signal_handler)
        opt_usage = "usage: \n  DATA | python %s SWARM_ID RESOURCE_ID FEED_NAME"%(sys.argv[1])
        opt_usage += "\n\n  *DATA: The data to produce in the Feed. Valid forms; \"echo 'data here'\", \"cat <filename>\"." \
                    +"\n  *SWARM_ID: The ID of the Swarm to produce to. This is a really long, unique identifier." \
                    +"\n  *RESOURCE_ID: The ID of the Resource to produce with. This is the \"id\" field in the resource's listed JSON." \
                    +"\n  *FEED_NAME: The name of the Feed you are producing."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        if len(args) != 4:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        swarm_id = args[1]
        resource_id = args[2]
        feed_name = args[3]
        produce(server_info["hostname"], keys["producer"], swarm_id, resource_id, feed_name)
    else:
        usage(sys.argv[0])

main()
