#!/usr/bin/python
import swarmtoolscore
import sys
import httplib
import json

def usage(name):
    print "%s [create|list|destroy] options"%(name)
    sys.exit()

def usage_create(name):
    print "%s create NAME DESCRIPTION [--public]"%(name)
    sys.exit()

def usage_destroy(name):
    print "%s destroy SWARM_ID"%(name)
    sys.exit()

def create_swarm(api_key, name, description, public):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    new_swarm_json = json.dumps({'name': name, 
                                 'description': description, 
                                 'public': public})
    print "new_swarm_json", new_swarm_json
    conn.request("POST", "/swarms", new_swarm_json, {"x-bugswarmapikey": api_key, "content-type": "application/json"})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def list_swarms(api_key):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("GET", "/swarms", None, {"x-bugswarmapikey": api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def destroy_swarm(api_key, swarm_id):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("DELETE", "/swarms/%s"%(swarm_id), None, {"x-bugswarmapikey": api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print txt

def main():
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) == 1:
        usage(sys.argv[0]);
    if sys.argv[1] == "list":
        list_swarms(keys["master"])
    elif sys.argv[1] == "create":
        if len(sys.argv) < 4:
            usage_create(sys.argv[0])
        name = sys.argv[2]
        description = sys.argv[3]
        public = False
        if (len(sys.argv) > 3):
            public = (sys.argv.count("--public") > 0)
        create_swarm(keys["master"], name, description, public)
    elif sys.argv[1] == "destroy":
        if len(sys.argv) < 3:
            usage_destroy(sys.argv[0])
        swarm_id = sys.argv[2]
        destroy_swarm(keys["master"], swarm_id)
    else:
        print "Command '%s' is invalid"%(sys.argv[1])
        usage(sys.argv[0])
main()
