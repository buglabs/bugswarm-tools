#!/usr/bin/python
from optparse import OptionParser
import swarmtoolscore
import sys
import httplib
import json
import base64
import init

def usage(script_name):
    print "%s [create|list] \n"%(script_name)
    print "Use '%s [method] --help' for a method's usage and options."%(script_name)
    sys.exit()
 
def create(user_id, options, args):
    if len(args) != 2:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    password = args[1]
    conn = httplib.HTTPConnection('api.bugswarm.net')
    auth_hash = user_id + ":" + password
    auth_header = "Basic " + base64.b64encode(auth_hash)
    if (options.key_type != None):
        conn.request("POST", "/keys/" + options.key_type, None, {"Authorization":auth_header})
    else:
        conn.request("POST", "/keys", None, {"Authorization":auth_header})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)
    init.init(user_id, password)

def list(user_id, args):
    if len(args) != 2:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    password = args[1]
    conn = httplib.HTTPConnection('api.bugswarm.net')
    auth_hash = user_id + ":" + password
    auth_header = "Basic " + base64.b64encode(auth_hash)
    conn.request("GET", "/keys", None, {"Authorization":auth_header})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def main():
    user_info = swarmtoolscore.get_user_info()
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    elif sys.argv[1] == "create":
        opt_usage = "usage: %s <password> [options]"%(sys.argv[1])
        parser = OptionParser(usage = opt_usage)
        parser.add_option("-t", "--type", dest="key_type", help="Specify the type of API key; 'master', 'producer', 'consumer' (master is used by default)", metavar="<key_type>")
        (options, args) =  parser.parse_args()
        create(user_info["user_id"], options, args)
    elif sys.argv[1] == "list":
        opt_usage = "usage: %s <password>"%(sys.argv[1])
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        list(user_info["user_id"], args)
    else:
        usage(sys.argv[0])
main()
