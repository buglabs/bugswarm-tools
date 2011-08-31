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

def create(api_key, options, args):
    if len(args) != 3:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    name = args[1]
    description = args[2]
    conn = httplib.HTTPConnection('api.bugswarm.net')
    create_swarm = {"name": name, "description": description}
    if options.public != None:
        create_swarm["public"] = options.public
    create_swarm_json = json.dumps(create_swarm)
    conn.request("POST", "/swarms", create_swarm_json, {"x-bugswarmapikey":api_key, "content-type":"application/json"})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def update(api_key, options, args):
    if len(args) != 2:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    swarm_id = args[1]
    conn = httplib.HTTPConnection('api.bugswarm.net')
    update_swarm = {}
    if options.name != None:
        update_swarm["name"] = options.name
    if options.description != None:
        update_swarm["description"] = options.description
    if options.public != None:
        update_swarm["public"] = options.public
    update_swarm_json = json.dumps(update_swarm)
    conn.request("PUT", "/swarms/%s"%(swarm_id), update_swarm_json, {"x-bugswarmapikey":api_key, "content-type":"application/json"})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print txt

def destroy(api_key, args):
    if len(args) != 2:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    swarm_id = args[1]
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("DELETE", "/swarms/%s"%(swarm_id), None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print txt

def list_user_swarms(api_key, args):
    if len(args) != 1:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("GET", "/swarms", None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def get_swarm_info(api_key, args):
    if len(args) != 2:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    swarm_id = args[1]
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
    if sys.argv[1] == "create":
        opt_usage = "usage: %s <name> <description> [options]"%(sys.argv[1])
        parser = OptionParser(usage = opt_usage)
        parser.add_option("-p", "--public", dest="public", help="Set whether the Swarm is public or not; 'true' or 'false'.", metavar="<public>")
        (options, args) = parser.parse_args()
        create(keys["master"], options, args)     
    if sys.argv[1] == "update":
        opt_usage = "usage: %s <swarm_id> [options]"%(sys.argv[1])
        parser = OptionParser(usage = opt_usage)
        parser.add_option("-n", "--name", dest="name", help="Set the Swarm's name", metavar="<name>")
        parser.add_option("-d", "--description", dest="description", help="Set the Swarm's description", metavar="<description>")
        parser.add_option("-p", "--public", dest="public", help="Set whether the Swarm is public or not; 'true' or 'false'.", metavar="<public>")
        (options, args) = parser.parse_args()
        update(keys["master"], options, args)
    if sys.argv[1] == "destroy":
        opt_usage = "usage: %s <swarm_id>"%(sys.argv[1])
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        destroy(keys["master"], args)
    if sys.argv[1] == "list_user_swarms":
        opt_usage = "usage: %s"%(sys.argv[1])
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        list_user_swarms(keys["master"], args)
    if sys.argv[1] == "get_swarm_info":
        opt_usage = "usage: %s <swarm_id>"%(sys.argv[1])
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        get_swarm_info(keys["master"], args)

main()
