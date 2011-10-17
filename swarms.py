#!/usr/bin/python
from optparse import OptionParser
from lib import swarmtoolscore
import sys
import httplib
import json
import ast

def usage(script_name):
    print "%s [create|update|destroy|list|get_swarm_info] \n"%(script_name)
    print "Use '%s [method] --help for a method's usage and options."%(script_name)
    sys.exit()

def create(hostname, api_key, name, description, public, resources):
    conn = httplib.HTTPConnection(hostname)
    create_swarm = {"name": name, "description": description}
    if public != None:
        if public == "true":
            create_swarm["public"] = True
        elif public == "false":
            create_swarm["public"] = False
    if resources != None:
        resources_dict = ast.literal_eval(resources)
        resources_list = []
        for key, value in resources_dict.iteritems():
            resource_dict = {"resource_id": key, "resource_type": value}
            resources_list.append(resource_dict)
        create_swarm["resources"] = resources_list
    create_swarm_json = json.dumps(create_swarm)
    conn.request("POST", "/swarms", create_swarm_json, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def update(hostname, api_key, swarm_id, name, description, public):
    conn = httplib.HTTPConnection(hostname)
    update_swarm = {}
    if name != None:
        update_swarm["name"] = name
    if description != None:
        update_swarm["description"] = description
    if public != None:
        if public == "true":
            update_swarm["public"] = True
        elif public == "false":
            update_swarm["public"] = False
    update_swarm_json = json.dumps(update_swarm)
    conn.request("PUT", "/swarms/%s"%(swarm_id), update_swarm_json, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def destroy(hostname, api_key, swarm_id):
    conn = httplib.HTTPConnection(hostname)
    conn.request("DELETE", "/swarms/%s"%(swarm_id), None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.status
    conn.close()
    if str(txt) == "204":
        print "Great success! :)"
    else:
        print txt
        print "Something went wrong! :("

def list_user_swarms(hostname, api_key):
    conn = httplib.HTTPConnection(hostname)
    conn.request("GET", "/swarms", None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def get_swarm_info(hostname, api_key, swarm_id):
    conn = httplib.HTTPConnection(hostname)
    conn.request("GET", "/swarms/%s"%(swarm_id), None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def main():
    server_info = swarmtoolscore.get_server_info()
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    elif sys.argv[1] == "create":
        opt_usage = "usage: \n  %s NAME DESCRIPTION [options]"%(sys.argv[1])
        opt_usage += "\n\n  *NAME: The name of the swarm being created." \
                    +"\n  *DESCRIPTION: The description of the swarm being created."
        parser = OptionParser(usage = opt_usage)
        parser.add_option("-p", "--public", dest="public", help="Set whether the swarm is public or not. Valid types; 'true', 'false'.", metavar="PUBLIC")
        parser.add_option("-r", "--resources", dest="resources", help="Input resources you wish to add to the swarm by default. Format the resources as a dictionary of 'resource_id:resource_type' key:value pairs.", metavar="RESOURCES")
        (options, args) = parser.parse_args()
        if len(args) != 3:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        name = args[1]
        description = args[2]
        create(server_info["hostname"], keys["configuration"], name, description, options.public, options.resources)     
    elif sys.argv[1] == "update":
        opt_usage = "usage: \n  %s SWARM_ID [options]"%(sys.argv[1])
        opt_usage += "\n\n  *SWARM_ID: The ID of the swarm being updated."
        parser = OptionParser(usage = opt_usage)
        parser.add_option("-n", "--name", dest="name", help="Set the swarm's name", metavar="NAME")
        parser.add_option("-d", "--description", dest="description", help="Set the swarm's description", metavar="DESCRIPTION")
        parser.add_option("-p", "--public", dest="public", help="Set whether the swarm is public or not. Valid types; 'true', 'false'.", metavar="PUBLIC")
        (options, args) = parser.parse_args()
        if len(args) != 2:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        swarm_id = args[1]
        update(server_info["hostname"], keys["configuration"], swarm_id, options.name, options.description, options.public)
    elif sys.argv[1] == "destroy":
        opt_usage = "usage: \n  %s SWARM_ID"%(sys.argv[1])
        opt_usage += "\n\n  *SWARM_ID: The ID of the swarm to destroy."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        if len(args) != 2:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        swarm_id = args[1]
        destroy(server_info["hostname"], keys["configuration"], swarm_id)
    elif sys.argv[1] == "list":
        opt_usage = "usage: \n  %s"%(sys.argv[1])
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        if len(args) != 1:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        list_user_swarms(server_info["hostname"], keys["configuration"])
    elif sys.argv[1] == "get_swarm_info":
        opt_usage = "usage: \n  %s SWARM_ID"%(sys.argv[1])
        opt_usage += "\n\n  *SWARM_ID: The ID of the swarm who's info is desired."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        if len(args) != 2:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        swarm_id = args[1]
        get_swarm_info(server_info["hostname"], keys["configuration"], swarm_id)
    else:
        usage(sys.argv[0])
main()
