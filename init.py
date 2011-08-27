#!/usr/bin/python
import ConfigParser
import sys
import httplib
import json
import base64


def usage(name):
    print "%s [init <username> <password>]"%(name)
    sys.exit()

def init(username, password):
    config = ConfigParser.ConfigParser()

    add_keys(username, password, config)
    
    with open("swarm.cfg", "wb") as configfile:
        config.write(configfile)

def add_keys(username, password, config):
    config.add_section("Keys")
    conn = httplib.HTTPConnection('api.bugswarm.net')
    auth_hash = username + ":" + password
    auth_header = "Basic " + base64.b64encode(auth_hash)
    conn.request("GET", "/keys", None, {"Authorization":auth_header})
    resp = conn.getresponse()
    txt = resp.read()
    print txt
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
    if len(sys.argv) == 1 and sys.argv[0] == "init.py":
        usage(sys.argv[0])
    elif sys.argv[0] == "init.py" and sys.argv[1] == "init":
        init(sys.argv[2], sys.argv[3])

main()
