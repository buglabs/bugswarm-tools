#!/usr/bin/python
from optparse import OptionParser
import swarmtoolscore
import sys
import httplib
import json

def usage(script_name):
    print "%s [create|update|destroy|list_user_resources|get_resource_info|list_swarms_with_resource] \n"%(script_name)
    print "Use '%s [method] --help for a method's usage and options."%(script_name)
    sys.exit()

def create(api_key, options, args):
    if len(args) != 4:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    resource_id = args[1]
    name = args[2]
    machine_type = args[3]
    create_resource = {"id": resource_id, "name": name, "machine_type": machine_type}
    if options.description != None:
        create_resource["description"] = options.description
    if options.position != None:
        create_resource["position"] = options.position
    create_resource_json = json.dumps(create_resource)
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("POST", "/resources", create_resource_json, {"x-bugswarmapikey":api_key, "content-type":"application/json"})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print txt

def update(api_key, options, args):
    if len(args) != 2:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    resource_id = args[1]
    update_resource = {}
    if options.name != None:
        update_resource["name"] = options.name
    if options.machine_type != None:
        update_resource["machine_type"] = options.machine_type
    if options.description != None:
        update_resource["description"] = options.description
    if options.position != None:
        update_resource["position"] = options.position
    update_resource_json = json.dumps(update_resource)
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("PUT", "/resources/%s"%(resource_id), update_resource_json, {"x-bugswarmapikey":api_key, "content-type":"application/json"})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print txt

def destroy(api_key, args):
    if len(args) != 2:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    resource_id = args[1]
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("DELETE", "/resources/%s"%(resource_id), None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print txt

def list_user_resources(api_key, args):
    if len(args) != 1:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("GET", "/resources", None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def get_resource_info(api_key, args):
    if len(args) != 2:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    resource_id = args[1]
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("GET", "/resources/%s"%(resource_id), None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def list_swarms_with_resource(api_key, args):
    if len(args) != 2:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    resource_id = args[1]
    conn = httplib.HTTPConnection('api.bugswarm.net')
    conn.request("GET", "/resources/%s/swarms"%(resource_id), None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def main():
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    elif sys.argv[1] == "create":
        opt_usage = "usage: %s <resource_id> <name> <machine_type> [options]"%(sys.argv[1])
        parser = OptionParser(usage = opt_usage)
        parser.add_option("-d", "--description", dest="description", help="Set the Resource's description", metavar="<description>")
        parser.add_option("-p", "--position", dest="position", help="Set the Resource's position", metavar="{\"longitude\":<value>, \"latitude\":<value>}")
        (options, args) = parser.parse_args()
        create(keys["master"], options, args)
    elif sys.argv[1] == "update":
        opt_usage = "usage: %s <resource_id> [options]"%(sys.argv[1])
        parser = OptionParser(usage = opt_usage)
        parser.add_option("-n", "--name", dest="name", help="Set the Resource's name", metavar="<name>")
        parser.add_option("-t", "--type", dest="machine_type", help="Set the Resource's machine type", metavar="<machine_type>")
        parser.add_option("-d", "--description", dest="description", help="Set the Resource's description", metavar="<description>")
        parser.add_option("-p", "--position", dest="position", help="Set the Resource's position", metavar="{\"longitude\":<value>, \"latitude\":<value>}")
        (options, args) = parser.parse_args()
        update(keys["master"], options, args)
    elif sys.argv[1] == "destroy":
        opt_usage = "usage: %s <resource_id>"%(sys.argv[1])
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        destroy(keys["master"], args)
    elif sys.argv[1] == "list_user_resources":
        opt_usage = "usage: %s"%(sys.argv[1])
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        list_user_resources(keys["master"], args)
    elif sys.argv[1] == "get_resource_info":
        opt_usage = "usage: %s <resource_id>"%(sys.argv[1])
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        get_resource_info(keys["master"], args)
    elif sys.argv[1] == "list_swarms_with_resource":
        opt_usage = "usage: %s <resource_id>"%(sys.argv[1])
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        list_swarms_with_resource(keys["master"], args)
    else:
        usage(sys.argv[0])
main()
