#!/usr/bin/python
from lib import apikey
from lib import resource
from lib import swarm
import logging

logging.basicConfig(level=logging.DEBUG)
print "\n"
api = apikey.apikey("atergis_dp","buglabs")
oldres = resource.getResources(api)[0]
swarms = oldres.getSwarms()
for swrm in swarms:
    print swrm.name
    for res in swrm.resources:
        print '    '+swrm.resources[res].name

