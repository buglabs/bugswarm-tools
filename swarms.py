#!/usr/bin/python
from optparse import OptionParser
import swarmtoolscore
import sys
import httplib
import json

def usage(script_name):
    print "%s [create|update|destroy|list_user_swarms|get_swarm_info] \n"%(script_name)
    print "Use '%s [method] --help for a method's usage and options."%(script_name)
    sys.exit()

def create(api_key, name, description, public):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    create_swarm = {"name": name, "description": description}
    if public != None:
        create_swarm["public"] = public
    create_swarm_json = json.dumps(create_swarm)
    conn.request("POST", "/swarms", create_swarm_json, {"x-bugswarmapikey":api_key, "content-type":"application/json"})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def update(api_key, swarm_id, name, description, public):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    update_swarm = {}
    if name != None:
        update_swarm["name"] = name
    if description != None:
        update_swarm["description"] = description
    if public != None:
        update_swarm["public"] = public
    update_swarm_json = json.dumps(update_swarm)
    conn.request("PUT", "/swarms/%s"%(swarm_id), update_swarm_json, {"x-bugswarmapikey":api_key, "content-type":"application/json"})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print txt

def destroy(api_key, swarm_id):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("DELETE", "/swarms/%s"%(swarm_id), None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print txt

def list_user_swarms(api_key):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("GET", "/swarms", None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def get_swarm_info(api_key, swarm_id):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("GET", "/swarms/%s"%(swarm_id), None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def main():
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    elif sys.argv[1] == "create":
        opt_usage = "usage: \n  %s NAME DESCRIPTION [options]"%(sys.argv[1])
        opt_usage += "\n\n  *NAME: The name of the Swarm being created." \
                    +"\n  *DESCRIPTION: The description of the Swarm being created."
        parser = OptionParser(usage = opt_usage)
        parser.add_option("-p", "--public", dest="public", help="Set whether the Swarm is public or not. Valid types; 'true', 'false'.", metavar="PUBLIC")
        (options, args) = parser.parse_args()
        if len(args) != 3:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        name = args[1]
        description = args[2]
        create(keys["master"], name, description, options.public)     
    elif sys.argv[1] == "update":
        opt_usage = "usage: \n  %s SWARM_ID [options]"%(sys.argv[1])
        opt_usage += "\n\n  *SWARM_ID: The ID of the Swarm being updated. This is a really long, unique identifier."
        parser = OptionParser(usage = opt_usage)
        parser.add_option("-n", "--name", dest="name", help="Set the Swarm's name", metavar="NAME")
        parser.add_option("-d", "--description", dest="description", help="Set the Swarm's description", metavar="DESCRIPTION")
        parser.add_option("-p", "--public", dest="public", help="Set whether the Swarm is public or not. Valid types; 'true', 'false'.", metavar="PUBLIC")
        (options, args) = parser.parse_args()
        if len(args) != 2:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        swarm_id = args[1]
        update(keys["master"], swarm_id, options.name, options.description, options.public)
    elif sys.argv[1] == "destroy":
        opt_usage = "usage: \n  %s SWARM_ID"%(sys.argv[1])
        opt_usage += "\n\n  *SWARM_ID: The ID of the Swarm to destroy. This is a really long, unique identifier."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        if len(args) != 2:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        swarm_id = args[1]
        destroy(keys["master"], swarm_id)
    elif sys.argv[1] == "list_user_swarms":
        opt_usage = "usage: \n  %s"%(sys.argv[1])
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        if len(args) != 1:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        list_user_swarms(keys["master"])
    elif sys.argv[1] == "get_swarm_info":
        opt_usage = "usage: \n  %s SWARM_ID"%(sys.argv[1])
        opt_usage += "\n\n  *SWARM_ID: The ID of the Swarm who's info is desired. This is a really long, unique indentifier."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        if len(args) != 2:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        swarm_id = args[1]
        get_swarm_info(keys["master"], swarm_id)
    else:
        usage(sys.argv[0])
main()
