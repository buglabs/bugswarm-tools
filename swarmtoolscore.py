#!/usr/bin/python
import ConfigParser
import os.path
my_working_directory = os.path.dirname(__file__)

def usage(name):
    print "%s [init <username> <password>]"%(name)
    sys.exit()

def get_keys():
    config = ConfigParser.ConfigParser()
    raw_data = config.read("%s/swarm.cfg"%(my_working_directory))
    master = config.get("Keys", "master")
    consumer = config.get("Keys", "consumer")
    producer = config.get("Keys", "producer")
    return {"master" : master, "consumer": consumer, "producer": producer}

#functionality currently not supported
def get_swarms():
    swarms = {}
    config = ConfigParser.ConfigParser()
    raw_data = config.read("%s/swarm.cfg"%(my_working_directory))
    for swarm in config.options("Swarms"):
        swarms[swarm] = config.get("Swarms", swarm)
    return swarms
