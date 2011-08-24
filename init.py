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
    config.add_section("Settings")

    conn = httplib.HTTPConnection('api.bugswarm.net')
    auth_hash = username + ":" + password
    auth_header = "Basic " + base64.b64encode(auth_hash)
    conn.request("GET", "/keys", None, {"Authorization":auth_header})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    json_obj = json.loads(txt)
    for key_obj in json_obj:
        key_type = key_obj["type"]
        key_value = key_obj["key"]
        config.set("Settings", key_type, key_value)
    if config.has_option("Settings", "master") == False:
        config.set("Settings", "master", "none")
    if config.has_option("Settings", "consumer") == False:
        config.set("Settings", "consumer", "none")
    if config.has_option("Settings", "producer") == False:
        config.set("Settings", "producer", "none")
    with open("swarm.cfg", "wb") as configfile:
        config.write(configfile)    


def main():
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    if sys.argv[1] == "init":
        init(sys.argv[2], sys.argv[3])

main()
