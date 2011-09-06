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

def add(api_key, swarm_id, user_id, resource_id, type):
    add_resource = {"user_id": user_id, "resource": resource_id, "type": type}
    add_resource_json = json.dumps(add_resource)
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("POST", "/swarms/%s/resources"%(swarm_id), add_resource_json, {"x-bugswarmapikey":api_key, "content-type":"application/json"})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print txt

def remove(api_key, swarm_id, user_id, resource_id, type):
    remove_resource = {"user_id": user_id, "resource": resource_id, "type": type}
    remove_resource_json = json.dumps(remove_resource)
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("DELETE", "/swarms/%s/resources"%(swarm_id), remove_resource_json, {"x-bugswarmapikey":api_key, "content-type":"application/json"})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print txt

def list_swarm_resources(api_key, swarm_id, type):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    if type != None:
        if type == "producer" or type == "consumer" or type == "both":
            print "/swarms/%s/resource?type=%s"%(swarm_id, type)
            conn.request("GET", "/swarms/%s/resources?type=%s"%(swarm_id, type), None, {"x-bugswarmapikey":api_key})
        else:
            print "Invalid type. Option must be 'producer', 'consumer', or 'both'."
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
        opt_usage = "usage: \n  %s SWARM_ID USER_ID RESOURCE_ID TYPE"%(sys.argv[1])
        opt_usage += "\n\n  *SWARM_ID: The ID of the Swarm to add to. This is a really long, unique identifier." \
                    +"\n  *USER_ID: The ID of the User who's resource is being added." \
                    +"\n  *RESOURCE_ID: The ID of the Resource to add. This is the \"id\" field in the Resource's listed JSON." \
                    +"\n  *TYPE: The type of the Resource to add. Valid types; 'producer', 'consumer', 'both'."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        if len(args) != 5:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        swarm_id = args[1]
        user_id = args[2]
        resource_id = args[3]
        type = args[4]
        add(keys["master"], swarm_id, user_id, resource_id, type)
    elif sys.argv[1] == "remove":
        opt_usage = "usage: \n  %s SWARM_ID USER_ID RESOURCE_ID TYPE"%(sys.argv[1])
        opt_usage += "\n\n  *SWARM_ID: The ID of the Swarm remove from. This is a really long, unique identifier." \
                    +"\n  *USER_ID: The ID of the User who's resource is being removed." \
                    +"\n  *RESOURCE_ID: The ID of the Resource to remove. This is the \"id\" field in the Resource's listed JSON." \
                    +"\n  *TYPE: The type of the Resource to remove. Valid types; 'producer', 'consumer', 'both'."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        if len(args) != 5:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        swarm_id = args[1]
        user_id = args[2]
        resource_id = args[3]
        type = args[4]
        remove(keys["master"], swarm_id, user_id, resource_id, type)
    elif sys.argv[1] == "list_swarm_resources":
        opt_usage = "usage: \n  %s SWARM_ID [options]"%(sys.argv[1])
        opt_usage += "\n\n  *SWARM_ID: The ID of the Swarm who's Resources will be listed."
        parser = OptionParser(usage = opt_usage)
        parser.add_option("-t", "--type", dest="type", help="Limit the list. Valid types; 'producer', 'consumer', 'both'.", metavar="TYPE")
        (options, args) = parser.parse_args()
        if len(args) != 2:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        swarm_id = args[1]
        list_swarm_resources(keys["master"], swarm_id, options.type)
    else:
        usage(sys.argv[0])
main()
