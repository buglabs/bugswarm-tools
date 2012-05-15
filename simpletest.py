#!/usr/bin/python
from BUGswarm import apikey
from BUGswarm import resource
from BUGswarm import swarm
from BUGswarm import participation
import logging
import time

def presence(message):
    print "presence from "+message['from']['resource']

logging.basicConfig(level=logging.INFO)
print "\n"
api = apikey.apikey("demo","buglabs55")
res = resource.getResourceByName(api,"Renesas01")
swarms = res.getSwarms()
print "Press enter to quit"
pt = participation.participationThread(api,res, swarms, onPresence=presence)

try:
    raw_input("")
except KeyboardInterrupt:
    pass
pt.stop()
