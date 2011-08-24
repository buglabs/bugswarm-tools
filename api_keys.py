#!/usr/bin/python
import swarmtoolscore
import sys
import httplib
import json
import base64

def usage(name):
    print "%s [list <username> <password>]"%(name)
    sys.exit()

def list_keys(username, password):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    auth_hash = username + ":" + password
    auth_header = "Basic " + base64.b64encode(auth_hash)
    conn.request("GET", "/keys", None, {"Authorization":auth_header})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def main():
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    if sys.argv[1] == "list":
        list_keys(sys.argv[2], sys.argv[3])

main()
