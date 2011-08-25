#!/usr/bin/python
import swarmtoolscore
import sys
import httplib
import json

def usage(name):
    print "%s [invites]"%(name)
    sys.exit()

def list_invites(api_key):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("GET", "/invites", None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def main():
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    if sys.argv[1] == "list":
        list_invites(keys["master"])

main()
