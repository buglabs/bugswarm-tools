#!/usr/bin/python
from optparse import OptionParser
import ConfigParser
import sys
import httplib
import json
import base64

def usage(script_name):
    print "%s [init] \n"%(script_name)
    print "Use '%s [method] --help' for a method's usage and options."%(script_name)
    sys.exit()

def init(args):
    if len(args) != 3:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    user_id = args[1]
    password = args[2]
    config = ConfigParser.ConfigParser()
    config.add_section("User Information")
    config.set("User Information", "user_id", user_id)

    add_keys(user_id, password, config)
    
    with open("swarm.cfg", "wb") as configfile:
        config.write(configfile)

def add_keys(user_id, password, config):
    config.add_section("Keys")
    conn = httplib.HTTPConnection('api.bugswarm.net')
    auth_hash = user_id + ":" + password
    auth_header = "Basic " + base64.b64encode(auth_hash)
    conn.request("GET", "/keys", None, {"Authorization":auth_header})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    json_obj = json.loads(txt)
    for key_obj in json_obj:
        key_type = key_obj["type"]
        key_value = key_obj["key"]
        config.set("Keys", key_type, key_value)
    if config.has_option("Keys", "master") == False:
        config.set("Keys", "master", "none")
    if config.has_option("Keys", "consumer") == False:
        config.set("Keys", "consumer", "none")
    if config.has_option("Keys", "producer") == False:
        config.set("Keys", "producer", "none")

def main():
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    if sys.argv[1] == "init":
        opt_usage = "usage: %s <user_id> <password>"%(sys.argv[1])
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        init(args)

    elif sys.argv[0] == "init.py" and sys.argv[1] == "init":
        init(sys.argv[2], sys.argv[3])
    else:
        usage(sys.argv[0])
>>>>>>> 345c5810bb1318dc24fbb7ad6cdc7e2662c7dbb7
main()
