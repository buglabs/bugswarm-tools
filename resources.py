#!/usr/bin/python
import swarmtoolscore
import sys
import httplib
import json

def usage(name):
    print "%s [list_swarm <Swarm id>|list_user|get <Resource id>|add <Swarm id> <type> <User id> <Resource id>|remove <Swarm id> <type> <User id> <Resource id>]"%s(name)
    sys.exit()

def list_swarm_resources(api_key, swarm_id):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("GET", "/swarms/%s/resources"%(swarm_id), None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def list_user_resources(api_key):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("GET", "/resources", None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def get_resource(api_key, resource_id):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("GET", "/resources/%s"%(resource_id), None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def add(api_key, swarm_id, resource_type, user_id, resource_id):
    new_resource_json = json.dumps({"type": resource_type, "user_id": user_id, "resource": resource_id})
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("POST", "/swarms/%s/resources"%(swarm_id), new_resource_json, {"x-bugswarmapikey":api_key, "content-type":"application/json"})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print txt

def remove(api_key, swarm_id, resource_type, user_id, resource_id):
    remove_resource_json = json.dumps({"type": resource_type, "user_id": user_id, "id": resource_id})
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("DELETE", "/swarms/%s/resources"%(swarm_id), remove_resource_json, {"x-bugswarmapikey":api_key, "content-type":"application/json"})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print txt

def main():
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    if sys.argv[1] == "list_swarm":
        list_swarm_resources(keys["master"], sys.argv[2])
    if sys.argv[1] == "list_user":
        list_user_resources(keys["master"])
    if sys.argv[1] == "get":
        get_resource(keys["master"], sys.argv[2])
    if sys.argv[1] == "add":
        add(keys["master"], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    if sys.argv[1] == "remove":
        remove(keys["master"], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

main()
