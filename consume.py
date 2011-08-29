import swarmtoolscore
import sys
import httplib
import os

def usage(name):
    print "%s SWARM_ID"%(name)
    sys.exit()

def consume(api_key, swarm_id):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("GET", "/stream?swarm_id=%s"%(swarm_id), None, {"x-bugswarmapikey": api_key, "Connection": "keep-alive"})
    resp = conn.getresponse()
    while(1):
        txt = resp.read(1)
        sys.stdout.write(txt)
    conn.close();

def main():
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) != 2:
        usage(sys.argv[0])
    swarm_id = sys.argv[1]
    consume(keys["consumer"], swarm_id)

main()
