#!/usr/bin/python
from BUGswarm import apikey
from BUGswarm import resource
from BUGswarm import participation
import logging

logging.basicConfig(level=logging.INFO)
api = apikey.apikey("demo","buglabs55")
res = resource.getResourceByName(api,"Renesas01")
swarms = res.getSwarms()

print "Press enter to quit"

def presence(obj):
    print "presence from "+obj['from']['resource']
def message(obj):
    print "message "+str(obj['payload'])
def error(obj):
    print "error "+str(obj['errors'])

pt = participation.participationThread(api,res, swarms,
        onPresence=presence, onMessage=message, onError=error)

try:
    raw_input("")
except KeyboardInterrupt:
    pass
pt.stop()
