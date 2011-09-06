#!/usr/bin/python
import ConfigParser
import os.path
import httplib
import base64
import json
my_working_directory = os.path.dirname(__file__)

def get_keys():
    config = ConfigParser.ConfigParser()
    raw_data = config.read("%s/swarm.cfg"%(my_working_directory))
    master = config.get("Keys", "master")
    consumer = config.get("Keys", "consumer")
    producer = config.get("Keys", "producer")
    return {"master" : master, "consumer": consumer, "producer": producer}

def get_user_info():
    config = ConfigParser.ConfigParser()
    raw_data = config.read("%s/swarm.cfg"%(my_working_directory))
    user_id = config.get("User Information", "user_id")
    return {"user_id": user_id}

def set_user_info(user_id):
    config = ConfigParser.ConfigParser()
    config.read("%s/swarm.cfg"%(my_working_directory))
    config.set("User Information", "user_id", user_id)

    with open("swarm.cfg", "wb") as configfile:
        config.write(configfile)

def set_keys(user_id, password):
    config = ConfigParser.ConfigParser()
    config.read("%s/swarm.cfg"%(my_working_directory))
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

    with open("swarm.cfg", "wb") as configfile:
        config.write(configfile)

