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

def usage_update(name):
    print "%s update SWARM_ID [DESCRIPTION] [--public|--private]"%(name)
    sys.exit()

def usage_destroy(name):
    print "%s destroy SWARM_ID"%(name)
    sys.exit()

def usage_list_swarms_with_resource(name):
    print "%s resource RESOURCE_ID"%(name)
    sys.exit()

def usage_swarm_info(name):
    print "%s info RESOURCE_ID"%(name)
    sys.exit()

def create_swarm(api_key, name, description, public):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    new_swarm_json = json.dumps({'name': name, 
                                 'description': description, 
                                 'public': public})
    conn.request("POST", "/swarms", new_swarm_json, {"x-bugswarmapikey": api_key, "content-type": "application/json"})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def update_swarm(api_key, swarm_id, changes):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    update_swarm_json = json.dumps(changes)
    print update_swarm_json
    conn.request("PUT", "/swarms/%s"%(swarm_id), update_swarm_json, {"x-bugswarmapikey": api_key,  "content-type": "application/json"})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print txt

def destroy_swarm(api_key, swarm_id):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("DELETE", "/swarms/%s"%(swarm_id), None, {"x-bugswarmapikey": api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print txt

def list_swarms(api_key):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("GET", "/swarms", None, {"x-bugswarmapikey": api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def list_swarms_with_resource(api_key, resource_id):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("GET", "/resources/%s/swarms"%(resource_id), None, {"x-bugswarmapikey": api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def swarm_info(api_key, swarm_id):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("GET", "/swarms/%s"%(swarm_id), None, {"x-bugswarmapikey": api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def main():
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) == 1:
        usage(sys.argv[0]);
    if sys.argv[1] == "create":
        if len(sys.argv) < 4:
            usage_create(sys.argv[0])
        name = sys.argv[2]
        description = sys.argv[3]
        public = False
        if (len(sys.argv) > 3):
            public = (sys.argv.count("--public") > 0)
        create_swarm(keys["master"], name, description, public)
    elif sys.argv[1] == "update":
        if len(sys.argv) < 3:
            usage_update(sys.argv[0])
        swarm_id = sys.argv[2]
        changes = {}
        if sys.argv.count("--public") > 0:
            changes["public"] = True
        elif sys.argv.count("--private") > 0:
            changes["public"] = False
        descriptions = [x for x in sys.argv[3:] if x != "--private" and x != "--public"]
        if len(descriptions) > 0:
            changes["description"] = descriptions[0]
        update_swarm(keys["master"], swarm_id, changes)
    elif sys.argv[1] == "destroy":
        if len(sys.argv) < 3:
            usage_destroy(sys.argv[0])
        swarm_id = sys.argv[2]
        destroy_swarm(keys["master"], swarm_id)
    elif sys.argv[1] == "list":
        list_swarms(keys["master"])
    elif sys.argv[1] == "resource":
        if len(sys.argv) < 3:
            usage_list_swarms_with_resource(sys.argv[0])
        resource_id = sys.argv[2]
        list_swarms_with_resource(keys["master"], resource_id)
    elif sys.argv[1] == "info":
        if len(sys.argv) < 3:
            usage_swarm_info(sys.argv[0])
        swarm_id = sys.argv[2]
        swarm_info(keys["master"], swarm_id)
    else:
        print "Command '%s' is invalid"%(sys.argv[1])
        usage(sys.argv[0])
main()
