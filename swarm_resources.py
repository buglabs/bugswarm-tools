#!/usr/bin/python
from optparse import OptionParser
from lib import swarmtoolscore
import sys
import httplib
import json

def usage(script_name):
    print "%s [add|remove|list] \n"%(script_name)
    print "Use '%s [method] --help for a method's usage and options."%(script_name)
    sys.exit()

def add(hostname, api_key, swarm_id, resource_id, resource_type):
    add_resource = {"resource_id": resource_id, "resource_type": resource_type}
    add_resource_json = json.dumps(add_resource)
    conn = httplib.HTTPConnection(hostname)
    conn.request("POST", "/swarms/%s/resources"%(swarm_id), add_resource_json, {"x-bugswarmapikey":api_key, "content-type":"application/json"})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    if txt != "Created":
        print json.dumps(json.loads(txt), sort_keys=True, indent=4)
    else:
        print "Great success! :)"

def remove(hostname, api_key, swarm_id, resource_id, resource_type):
    remove_resource = {"resource_id": resource_id, "resource_type": resource_type}
    remove_resource_json = json.dumps(remove_resource)
    conn = httplib.HTTPConnection(hostname)
    conn.request("DELETE", "/swarms/%s/resources"%(swarm_id), remove_resource_json, {"x-bugswarmapikey":api_key, "content-type":"application/json"})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    if txt != "":
        print json.dumps(json.loads(txt), sort_keys=True, indent=4)
    else: 
        print "Great success! :)"

def list_swarm_resources(hostname, api_key, swarm_id, resource_type):
    conn = httplib.HTTPConnection(hostname)
    if resource_type != None:
        if resource_type == "producer" or resource_type == "consumer" or resource_type == "both":
            conn.request("GET", "/swarms/%s/resources?type=%s"%(swarm_id, resource_type), None, {"x-bugswarmapikey":api_key})
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
    server_info = swarmtoolscore.get_server_info()
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    elif sys.argv[1] == "add":
        opt_usage = "usage: \n  %s SWARM_ID RESOURCE_ID RESOURCE_TYPE"%(sys.argv[1])
        opt_usage += "\n\n  *SWARM_ID: The ID of the swarm to add to." \
                    +"\n  *RESOURCE_ID: The ID of the resource to add." \
                    +"\n  *RESOURCE_TYPE: The type of the resource to add. Valid types; 'producer', 'consumer', 'both'."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        if len(args) != 4:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        swarm_id = args[1]
        resource_id = args[2]
        resource_type = args[3]
        add(server_info["hostname"], keys["master"], swarm_id, resource_id, resource_type)
    elif sys.argv[1] == "remove":
        opt_usage = "usage: \n  %s SWARM_ID RESOURCE_ID RESOURCE_TYPE"%(sys.argv[1])
        opt_usage += "\n\n  *SWARM_ID: The ID of the rwarm remove from." \
                    +"\n  *RESOURCE_ID: The ID of the resource to remove." \
                    +"\n  *RESOURCE_TYPE: The type of the resource to remove. Valid types; 'producer', 'consumer', 'both'."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        if len(args) != 4:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        swarm_id = args[1]
        resource_id = args[2]
        resource_type = args[3]
        remove(server_info["hostname"], keys["master"], swarm_id, resource_id, resource_type)
    elif sys.argv[1] == "list":
        opt_usage = "usage: \n  %s SWARM_ID [options]"%(sys.argv[1])
        opt_usage += "\n\n  *SWARM_ID: The ID of the swarm who's resources will be listed."
        parser = OptionParser(usage = opt_usage)
        parser.add_option("-t", "--type", dest="type", help="Limit the list. Valid types; 'producer', 'consumer', 'both'.", metavar="TYPE")
        (options, args) = parser.parse_args()
        if len(args) != 2:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        swarm_id = args[1]
        list_swarm_resources(server_info["hostname"], keys["master"], swarm_id, options.type)
    else:
        usage(sys.argv[0])
main()
