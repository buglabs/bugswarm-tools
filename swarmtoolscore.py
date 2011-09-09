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
    resp = get_keys_from_server(user_id, password)
    if resp.status == 404:
        print "Status is 404"
        create_key(user_id, password, "master")
        create_key(user_id, password, "producer")
        create_key(user_id, password, "consumer")
        resp = get_keys_from_server(user_id, password)
    txt = resp.read()
    json_obj = json.loads(txt)
    for key_obj in json_obj:
        key_type = key_obj["type"]
        key_value = key_obj["key"]
        config.set("Keys", key_type, key_value)

    if config.has_option("Keys", "master") == False:
        key_obj = create_key(user_id, password, "master")
        config.set("Keys", "master", key_obj["apikey"])
    if config.has_option("Keys", "producer") == False:
        key_obj = create_key(user_id, password, "producer")
        config.set("Keys", "producer", key_obj["apikey"])
    if config.has_option("Keys", "consumer") == False:
        key_obj = create_key(user_id, password, "consumer")
        config.set("Keys", "consumer", key_obj["apikey"])

    with open("swarm.cfg", "wb") as configfile:
        config.write(configfile)

def create_key(user_id, password, key_type):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    auth_hash = user_id + ":" + password
    auth_header = "Basic " + base64.b64encode(auth_hash)
    if (key_type != None):
        conn.request("POST", "/keys/" + key_type, None, {"Authorization":auth_header})
    else:
        conn.request("POST", "/keys", None, {"Authorization":auth_header})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    json_obj = json.loads(txt)
    return json_obj

def get_keys_from_server(user_id, password):
    conn = httplib.HTTPConnection('api.bugswarm.net')
    auth_hash = user_id + ":" + password
    auth_header = "Basic " + base64.b64encode(auth_hash)
    conn.request("GET", "/keys", None, {"Authorization":auth_header})
    resp = conn.getresponse()
    conn.close()
    return resp    
