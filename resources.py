#!/usr/bin/python
from optparse import OptionParser
from lib import swarmtoolscore
import sys
import httplib
import json

def usage(script_name):
    print "%s [create|update|destroy|list|get_info|list_swarms] \n"%(script_name)
    print "Use '%s [method] --help for a method's usage and options."%(script_name)
    sys.exit()

def create(hostname, api_key, name, machine_type, description, position):
    create_resource = {"name": name, "machine_type": machine_type}
    if description != None:
        create_resource["description"] = description
    if position != None:
        latitude = position[1]
        longitude = position[3]
        latlon = {"latitude": float(latitude), "longitude": float(longitude)}
        create_resource["position"] = latlon
    create_resource_json = json.dumps(create_resource)
    conn = httplib.HTTPConnection(hostname)
    conn.request("POST", "/resources", create_resource_json, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def update(hostname, api_key, resource_id, name, machine_type, description, position):
    update_resource = {}
    if name != None:
        update_resource["name"] = name
    if machine_type != None:
        update_resource["machine_type"] = machine_type
    if description != None:
        update_resource["description"] = description
    if position != None:
        latitude = position[1]
        longitude = position[3]
        latlon = {"latitude": int(latitude), "longitude": int(longitude)}
        update_resource["position"] = latlon
    update_resource_json = json.dumps(update_resource)
    conn = httplib.HTTPConnection(hostname)
    conn.request("PUT", "/resources/%s"%(resource_id), update_resource_json, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def destroy(hostname, api_key, resource_id):
    conn = httplib.HTTPConnection(hostname)
    conn.request("DELETE", "/resources/%s"%(resource_id), None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.status
    conn.close()
    if str(txt) == "204":
        print "Great success! :)"
    else:
        print "Something went wrong! :("
    
def list_resources(hostname, api_key):
    conn = httplib.HTTPConnection(hostname)
    conn.request("GET", "/resources", None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def get_info(hostname, api_key, resource_id):
    conn = httplib.HTTPConnection(hostname)
    conn.request("GET", "/resources/%s"%(resource_id), None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def list_swarms(hostname, api_key, resource_id):
    conn = httplib.HTTPConnection(hostname)
    conn.request("GET", "/resources/%s/swarms"%(resource_id), None, {"x-bugswarmapikey":api_key})
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
        opt_usage = "usage: \n  %s NAME MACHINE_TYPE [options]"%(sys.argv[1])
        opt_usage += "\n\n  *NAME: The name of the resource to create." \
                    +"\n  *MACHINE_TYPE: The machine type of the resource to create. Valid types; 'pc', 'smartphone', 'bug'."
        parser = OptionParser(usage = opt_usage)
        parser.add_option("-d", "--description", dest="description", help="Set the resource's description", metavar="DESCRIPTION")
        parser.add_option("-p", "--position", dest="position", help="Set the resource's position. Must be a tuple of floats surounded by quotations.", metavar="\"(LATITUDE, LONGITUDE)\"")
        (options, args) = parser.parse_args()
        if len(args) != 3:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        name = args[1]
        machine_type = args[2]
        create(server_info["hostname"], keys["configuration"], name, machine_type, options.description, options.position)
    elif sys.argv[1] == "update":
        opt_usage = "usage: \n  %s RESOURCE_ID [options]"%(sys.argv[1])
        opt_usage += "\n\n  *RESOURCE_ID: The ID of the resource to update."
        parser = OptionParser(usage = opt_usage)
        parser.add_option("-n", "--name", dest="name", help="Set the resource's name", metavar="NAME")
        parser.add_option("-t", "--type", dest="machine_type", help="Set the resource's machine type. Valid types; 'pc', 'smartphone', 'bug'.", metavar="MACHINE_TYPE")
        parser.add_option("-d", "--description", dest="description", help="Set the resource's description", metavar="DESCRIPTION")
        parser.add_option("-p", "--position", dest="position", help="Set the resource's position. Must be a tuple of floats surrounded by quotations.", metavar="\"(LATITUDE, LONGITUDE)\"")
        (options, args) = parser.parse_args()
        if len(args) != 2:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        resource_id = args[1]
        update(server_info["hostname"], keys["configuration"], resource_id, options.name, options.machine_type, options.description, options.position)
    elif sys.argv[1] == "destroy":
        opt_usage = "usage: \n  %s RESOURCE_ID"%(sys.argv[1])
        opt_usage += "\n\n  *RESOURCE_ID: The ID of the resource to destroy."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        if len(args) != 2:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        resource_id = args[1]
        destroy(server_info["hostname"], keys["configuration"], resource_id)
    elif sys.argv[1] == "list":
        opt_usage = "usage: \n  %s"%(sys.argv[1])
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        if len(args) != 1:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        list_resources(server_info["hostname"], keys["configuration"])
    elif sys.argv[1] == "get_info":
        opt_usage = "usage: \n  %s RESOURCE_ID"%(sys.argv[1])
        opt_usage += "\n\n  *RESOURCE_ID: The ID of the resource who's info is desired."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        if len(args) != 2:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        resource_id = args[1]
        get_info(server_info["hostname"], keys["configuration"], resource_id)
    elif sys.argv[1] == "list_swarms":
        opt_usage = "usage: \n  %s RESOURCE_ID"%(sys.argv[1])
        opt_usage += "\n\n  *RESOURCE_ID: The ID of the resource. The swarms that the resource is a member of will be listed."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        if len(args) != 2:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        resource_id = args[1]
        list_swarms(server_info["hostname"], keys["configuration"], resource_id)
    else:
        usage(sys.argv[0])
main()
