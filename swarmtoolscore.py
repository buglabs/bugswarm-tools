#!/usr/bin/python
import ConfigParser

def usage(name):
    print "%s [init <username> <password>]"%(name)
    sys.exit()

def get_keys():
    config = ConfigParser.ConfigParser()
    raw_data = config.read("swarm.cfg")
    master = config.get("Settings", "master")
    consumer = config.get("Settings", "consumer")
    producer = config.get("Settings", "producer")
    return {"master" : master, "consumer": consumer, "producer": producer}

