#!/usr/bin/python
import swarmtoolscore
import sys
import httplib
import json

def usage(name):
    print "%s [push <Resource id> <Feed id> <Swarm id>]"%(name)
    sys.exit()

def push_feed(api_key, resource_id, feed_id, swarm_id):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("PUT", "/resource/%s/feeds/%s?swarm_id=%s"%(resource_id, feed_id, swarm_id, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close
    print txt

def main():
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) == 1
        usage(sys.argv[0])
    if sys.argv[1] == "push":
        push_feed(keys["master"], sys.argv[2], sys.argv[3], sys.argv[4])

main()
