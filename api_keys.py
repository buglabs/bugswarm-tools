#!/usr/bin/python
import swarmtoolscore
import sys
import httplib
import json
import base64
import init

def usage(name):
    print "%s [generate <username> <password> <key type>|list <username> <password>|verify <key type>]"%(name)
    sys.exit()

def generate(username, password, key_type):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    auth_hash = username + ":" + password
    auth_header = "Basic " + base64.b64encode(auth_hash)
    conn.request("POST", "/keys/" + key_type, None, {"Authorization":auth_header})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)
    init.init(username, password)

def list_keys(username, password):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    auth_hash = username + ":" + password
    auth_header = "Basic " + base64.b64encode(auth_hash)
    conn.request("GET", "/keys", None, {"Authorization":auth_header})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def verify(key_type):
    keys = swarmtoolscore.get_keys()
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("GET", "/keys/" + keys[key_type] + "/verify", None, {"x-bugswarmapikey":keys["master"]})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print txt

def main():
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    if sys.argv[1] == "generate":
        generate(sys.argv[2], sys.argv[3], sys.argv[4])
    if sys.argv[1] == "list":
        list_keys(sys.argv[2], sys.argv[3])
    if sys.argv[1] == "verify":
        verify(sys.argv[2])

main()
