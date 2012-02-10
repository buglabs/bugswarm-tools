#!/usr/bin/python
import ConfigParser
import os.path
import httplib
import base64
import json
my_working_directory = os.path.abspath(os.path.dirname(__file__)+"/../")

def get_server_info():
    config = ConfigParser.ConfigParser()
    raw_data = config.read("%s/swarm.cfg"%(my_working_directory))
    hostname = config.get("Server Information", "hostname")
    return {"hostname": hostname}

def get_user_info():
    config = ConfigParser.ConfigParser()
    raw_data = config.read("%s/swarm.cfg"%(my_working_directory))
    user_id = config.get("User Information", "user_id")
    return {"user_id": user_id}

def get_keys():
    config = ConfigParser.ConfigParser()
    raw_data = config.read("%s/swarm.cfg"%(my_working_directory))
    configuration = config.get("Keys", "configuration")
    participation = config.get("Keys", "participation")
    return {"configuration": configuration, "participation": participation}

def set_server_info(hostname):
    config = ConfigParser.ConfigParser()
    config.read("%s/swarm.cfg"%(my_working_directory))
    config.set("Server Information", "hostname", hostname)

    with open("swarm.cfg", "wb") as configfile:
        config.write(configfile)
        
def set_user_info(user_id):
    config = ConfigParser.ConfigParser()
    config.read("%s/swarm.cfg"%(my_working_directory))
    config.set("User Information", "user_id", user_id)

    with open("swarm.cfg", "wb") as configfile:
        config.write(configfile)

def set_keys(hostname, user_id, password):
    config = ConfigParser.ConfigParser()
    config.read("%s/swarm.cfg"%(my_working_directory))
    resp = get_keys_from_server(hostname, user_id, password)
    if resp.status == 404:
        print "Status is 404"
        create_key(hostname, user_id, password, "configuration")
        create_key(hostname, user_id, password, "participation")
        resp = get_keys_from_server(hostname, user_id, password)
    txt = resp.read()
    print txt
    print resp.status
    if resp.status >= 400:
        print "Something bad happened: "
        print resp.status, txt
    json_obj = json.loads(txt)
    for key_obj in json_obj:
        key_type = key_obj["type"]
        key_value = key_obj["key"]
        config.set("Keys", key_type, key_value)

    if config.has_option("Keys", "configuration") == False:
        key_obj = create_key(hostname, user_id, password, "configuration")
        config.set("Keys", "configuration", key_obj["key"])
    if config.has_option("Keys", "participation") == False:
        key_obj = create_key(hostname, user_id, password, "participation")
        config.set("Keys", "participation", key_obj["key"])

    with open("swarm.cfg", "wb") as configfile:
        config.write(configfile)

def create_key(hostname, user_id, password, key_type):
    conn = httplib.HTTPConnection(hostname)
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

def get_keys_from_server(hostname, user_id, password):
    conn = httplib.HTTPConnection(hostname)
    auth_hash = user_id + ":" + password
    auth_header = "Basic " + base64.b64encode(auth_hash)
    print auth_header
    conn.request("GET", "/keys", None, {"Authorization":auth_header})
    resp = conn.getresponse()
    return resp    
