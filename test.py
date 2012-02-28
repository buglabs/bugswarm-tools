#!/usr/bin/python
from lib import apikey
from lib import resource
from lib import swarm
import logging

logging.basicConfig(level=logging.DEBUG)
api = apikey.apikey("atergis_dp","buglabs")
swrm = swarm.swarm(api, "82bf3639e5d52500bd3384efe6e9892b42ff6c0c")
print "\n"
for res in swrm.resources.values():
   print res.name+': '+str(res.permission)
#res = resource.getResources(api)[0]
#res.getSwarms()
#res = resource.resource.create(api,"pythontest01","DELETE ME")
#res.update("pythonsauce","DELETEMEMOAR")
#res.destroy()
