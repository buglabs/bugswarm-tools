#!/usr/bin/python
from optparse import OptionParser
import swarmtoolscore
import sys
import httplib
import json

def usage(script_name):
    print "%s [add|remove|list_swarm_resources] \n"%(script_name)
    print "Use '%s [method] --help for a method's usage and options."%(script_name)
    sys.exit()

def add(api_key, args):
    if len(args) != 5:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    swarm_id = args[1]
    user_id = args[2]
    resource_id = args[3]
    type = args[4]
    add_resource = {"user_id": user_id, "resource": resource_id, "type": type}
    add_resource_json = json.dumps(add_resource)
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("POST", "/swarms/%s/resources"%(swarm_id), add_resource_json, {"x-bugswarmapikey":api_key, "content-type":"application/json"})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print txt

def remove(api_key, args):
    if len(args) != 5:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    swarm_id = args[1]
    user_id = args[2]
    resource_id = args[3]
    type = args[4]
    remove_resource = {"user_id": user_id, "resource": resource_id, "type": type}
    remove_resource_json = json.dumps(remove_resource)
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("DELETE", "/swarms/%s/resources"%(swarm_id), remove_resource_json, {"x-bugswarmapikey":api_key, "content-type":"application/json"})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print txt

def list_swarm_resources(api_key, options, args):
    if len(args) != 2:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    swarm_id = args[1]
    conn = httplib.HTTPConnection('api.bugswarm.net')
    if options.type != None:
        if options.type == "producer":
            conn.request("GET", "/swarms/%s/resource?type=producer"%(swarm_id), None, {"x-bugswarmapikey":api_key})
        if options.type == "consumer":
            conn.request("GET", "/swarms/%s/resource?type=consumer"%(swarm_id), None, {"x-bugswarmapikey":api_key})
        else:
            print "Invalid type. Option must be 'producer' or 'consumer'."
            sys.exit()
    else:
        conn.request("GET", "/swarms/%s/resources"%(swarm_id), None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def main():
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    elif sys.argv[1] == "add":
        opt_usage = "usage: %s <swarm_id> <user_id> <resource_id> <type>"%(sys.argv[1])
        opt_usage += "\n*swarm_id: The ID of the Swarm to add to. This is a really long, unique identifier." \
                    +"\n*user_id: The ID of the User who's resource is being added." \
                    +"\n*resource_id: The ID of the Resource to add. This is the \"id\" field in the Resource's listed JSON." \
                    +"\n*type: The type of the Resource to add. Valid types; 'producer', 'consumer'."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        add(keys["master"], args)
    elif sys.argv[1] == "remove":
        opt_usage = "usage: %s <swarm_id> <user_id> <resource_id> <type>"%(sys.argv[1])
        opt_usage += "\n*swarm_id: The ID of the Swarm remove from. This is a really long, unique identifier." \
                    +"\n*user_id: The ID of the User who's resource is being removed." \
                    +"\n*resource_id: The ID of the Resource to remove. This is the \"id\" field in the Resource's listed JSON." \
                    +"\n*type: The type of the Resource to remove. Valid types; 'producer', 'consumer'."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        remove(keys["master"], args)
    elif sys.argv[1] == "list_swarm_resources":
        opt_usage = "usage: %s <swarm_id> [options]"%(sys.argv[1])
        opt_usage += "\n*swarm_id: The ID of the Swarm who's Resources will be listed."
        parser = OptionParser(usage = opt_usage)
        parser.add_option("-t", "--type", dest="type", help="Limit the list. Valid types; 'producer', 'consumer'.", metavar="<type>")
        (options, args) = parser.parse_args()
        list_swarm_resources(keys["master"], options, args)
    else:
        usage(sys.argv[0])
main()
