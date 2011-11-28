#!/usr/bin/python
from optparse import OptionParser
from lib import swarmtoolscore
import sys
import httplib
import os
import time
import signal

conn = None;

def usage(script_name):
    print "%s [produce] \n"%(script_name)
    print "Use '%s [method] --help' for a method's usage and options."%(script_name)
    sys.exit()

def signal_handler(signal, frame):
        global conn
        conn.close()
        print 'Http connection closed.'
        sys.exit(0)

def produce(hostname, api_key, swarm_id, resource_id, wrap):
    global conn
    conn = httplib.HTTPConnection(hostname)
    sel = "/stream?swarm_id=%s&resource_id=%s"%(swarm_id, resource_id)
    conn.putrequest("POST", sel)
    conn.putheader("x-bugswarmapikey", api_key)
    conn.putheader("transfer-encoding", "chunked")
    conn.putheader("connection", "keep-alive")
    conn.endheaders()

    #Sleep required to allow the swarm server time to respond with header
    #TODO - actually wait until header is returned
    time.sleep(1)
    if wrap == False:
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

        time.sleep(5)
        conn.send("0\r\n")
        time.sleep(5)
        conn.close()
    else:
        while True:
            try:
                payload = sys.stdin.readline()
                if (len(payload) < 1):
                    break
                msg = '{"message": {"to": ["' + swarm_id + '"], "payload": ' + payload + '}}'
                size = hex(len(msg))[2:] + "\r\n"
                chunk = msg + "\r\n"
                conn.send(size+chunk)
            except Exception as e:
                print "some sort of problem", e

        time.sleep(5)
        conn.send("0\r\n")
        time.sleep(5)
        conn.close()

def main():
    server_info = swarmtoolscore.get_server_info()
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    elif sys.argv[1] == "produce":
        signal.signal(signal.SIGINT, signal_handler)
        opt_usage = "usage: \n  DATA | ./produce.py %s SWARM_ID RESOURCE_ID [options]"%(sys.argv[1])
        opt_usage += "\n\n  *DATA: The data to produce in the feed. Valid forms; \"echo 'DATA'\", \"cat FILENAME\"." \
                    +"\n  *SWARM_ID: The ID of the swarm to produce to." \
                    +"\n  *RESOURCE_ID: The ID of the resource to produce with."
        parser = OptionParser(usage = opt_usage)
        parser.add_option("-w", action="store_true", dest="wrap", help="Wrap the payload in the proper message stanza.", default=False) 
        (options, args) = parser.parse_args()
        if len(args) != 3:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        swarm_id = args[1]
        resource_id = args[2]
        produce(server_info["hostname"], keys['participation'], swarm_id, resource_id, options.wrap)
    else:
        usage(sys.argv[0])

main()
