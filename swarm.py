#!/usr/bin/python
import swarmtoolscore
import sys
import httplib
import json

def usage(name):
    print "%s [create|list|delete]"%(name)
    sys.exit()

def create_swarm():
    pass

def list_swarms(api_key):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("GET", "/swarms", None, {"x-bugswarmapikey": api_key})
    resp = conn.getresponse();
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def delete_swarm():
    pass

def main():
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) == 1:
        usage(sys.argv[0]);
    if sys.argv[1] == "list":
        list_swarms(keys["master"])

main()
