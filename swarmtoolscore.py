#!/usr/bin/python
import ConfigParser
import os.path
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
