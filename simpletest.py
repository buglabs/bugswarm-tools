#!/usr/bin/python
from BUGswarm import apikey
from BUGswarm import resource
from BUGswarm import participation
import logging
import time

logging.basicConfig(level=logging.INFO)
api = apikey.apikey("demo","buglabs55")
res = resource.getResourceByName(api,"Renesas01")
swarms = res.getSwarms()

print "Press Control-C to quit\r\n"

def presence(obj):
    print "presence from "+obj['from']['resource']
def message(obj):
    print "message "+str(obj['payload'])
def error(obj):
    print "error "+str(obj['errors'])

pt = participation.participationThread(api,res, swarms,
        onPresence=presence, onMessage=message, onError=error)
try:
    while(True):
        pt.produce('{"data":"Hello world!"}')
        time.sleep(2)
except KeyboardInterrupt:
    pass
pt.stop()
