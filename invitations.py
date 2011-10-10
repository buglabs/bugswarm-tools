#!/usr/bin/python
from optparse import OptionParser
from lib import swarmtoolscore
import sys
import httplib
import json

def usage(script_name):
    print "%s [send|list_sent_invitations|list_received_invitations|respond] \n"%(script_name)
    print "Use '%s [method] --help for a method's usage and options."%(script_name)
    sys.exit()

def send(hostname, api_key, swarm_id, to, resource_id, resource_type, description):
    conn = httplib.HTTPConnection(hostname)
    invitation = {"to": to, "resource_id": resource_id, "resource_type": resource_type}
    if description != None:
        invitation["description"] = description
    invitation_json = json.dumps(invitation)
    conn.request("POST", "/swarms/%s/invitations"%(swarm_id), invitation_json, {"x-bugswarmapikey":api_key, "content-type":"application/json"})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def list_sent_invitations(hostname, api_key, swarm_id):
    conn = httplib.HTTPConnection(hostname)
    conn.request("GET", "/swarms/%s/invitations"%(swarm_id), None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def list_received_invitations(hostname, api_key, resource_id):
    conn = httplib.HTTPConnection(hostname)
    if resource_id != None:
        conn.request("GET", "/resources/%s/invitations"%(resource_id), None, {"x-bugswarmapikey":api_key})
    else:
        conn.request("GET", "/invitations", None, {"x-bugswarmapikey":api_key})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def respond(hostname, api_key, resource_id, invitation_id, status):
    conn = httplib.HTTPConnection(hostname)
    if status != "accept" and status != "reject":
        print "Invalid status. Must be 'accept' or 'reject'."
        sys.exit()
    response = {"status": status}
    response_json = json.dumps(response)
    conn.request("PUT", "/resources/%s/invitations/%s"%(resource_id, invitation_id), response_json, {"x-bugswarmapikey":api_key, "content-type":"application/json"})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def main():
    server_info = swarmtoolscore.get_server_info()
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    elif sys.argv[1] == "send":
        opt_usage = "usage: \n  %s SWARM_ID TO RESOURCE_ID RESOURCE_TYPE [options]"%(sys.argv[1])
        opt_usage += "\n\n  *SWARM_ID: The ID of the swarm that is inviting." \
                    +"\n  *TO: The username of the owner of the resource being invited." \
                    +"\n  *RESOURCE_ID: The ID of the resource being invited." \
                    +"\n  *RESOURCE_TYPE: The type that the invited resource would have presence as in the inviting swarm. Valid types; 'producer', 'consumer', 'both'."
        parser = OptionParser(usage = opt_usage)
        parser.add_option("-d", "--description", dest="description", help="Set a descriptive message to accompany the invitation.", metavar="DESCRIPTION")
        (options, args) = parser.parse_args()
        if len(args) != 5:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        swarm_id = args[1]
        to = args[2]
        resource_id = args[3]
        resource_type = args[4]
        send(server_info["hostname"], keys["master"], swarm_id, to, resource_id, resource_type, options.description)     
    elif sys.argv[1] == "list_sent_invitations":
        opt_usage = "usage: \n  %s SWARM_ID"%(sys.argv[1])
        opt_usage += "\n\n  *SWARM_ID: The ID of the swarm who's associated invitations will be listed."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        if len(args) != 2:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        swarm_id = args[1]
        list_sent_invitations(server_info["hostname"], keys["master"], swarm_id)
    elif sys.argv[1] == "list_received_invitations":
        opt_usage = "usage: \n  %s"%(sys.argv[1])
        parser = OptionParser(usage = opt_usage)
        parser.add_option("-r", "--resource", dest="resource_id", help="Specify a resource who's invitations you want to list.", metavar="RESOURCE_ID") 
        (options, args) = parser.parse_args()
        if len(args) != 1:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        list_received_invitations(server_info["hostname"], keys["master"], options.resource_id)
    elif sys.argv[1] == "respond":
        opt_usage = "usage: \n  %s RESOURCE_ID INVITATION_ID STATUS"%(sys.argv[1])
        opt_usage += "\n\n  *RESOURCE_ID: The ID of the resource who's invitation is being responded to." \
                    +"\n  *INVITATION_ID: The ID of the invitation being responded to." \
                    +"\n  *STATUS: The respose status. Valid types; 'accept', 'reject'."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        if len(args) != 4:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        resource_id = args[1]
        invitation_id = args[2]
        status = args[3]
        respond(server_info["hostname"], keys["master"], resource_id, invitation_id, status)
    else:
        usage(sys.argv[0])
main()
