import swarmtoolscore
import sys
import httplib
import os
import time

def usage(name):
    print "%s SWARM_ID RESOURCE_NAME FEED_NAME"%(name)
    print "Message are read from stdin, each message is one line long, messages are separated by newline characters"
    sys.exit()

def produce(api_key, swarm_id, resource_name, feed_name):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    #conn = httplib.HTTPConnection('127.0.0.1')
    sel = "/resources/%s/feeds/%s?swarm_id=%s"%(resource_name, feed_name, swarm_id)
    print sel
    print api_key
    conn.putrequest("PUT", sel)
    conn.putheader("X-BugSwarmApiKey", api_key)
    conn.putheader("Transfer-Encoding", "chunked")
    conn.endheaders()

    #time.sleep(1)
    #conn.send("1\r\n")
    #conn.send("1\r\n")
    #time.sleep(1)
    try:
        for msg in sys.stdin.readlines():
            stripped_msg = msg.strip()
            size = hex(len(stripped_msg))[2:] + "\r\n"
            chunk = stripped_msg + "\r\n"
            conn.send(size)
            conn.send(chunk)
            
    except Exception as e:
        print "some sort of problem", e

    conn.send("0\r\n")
    conn.close()

def main():
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) != 4:
        usage(sys.argv[0])
    swarm_id = sys.argv[1]
    resource_name = sys.argv[2]
    feed_name = sys.argv[3]
    produce(keys["producer"], swarm_id, resource_name, feed_name)

main()
