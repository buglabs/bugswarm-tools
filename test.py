#!/usr/bin/python
from lib import apikey
from lib import resource
from lib import swarm
import logging

logging.basicConfig(level=logging.DEBUG)
print "\n"
api = apikey.apikey("atergis_dp","buglabs")
res = resource.resource.create(api,"pythontest01","DELETE ME")
res.update("pythonsauce","DELETEMEMOAR")
res.permission = resource.resource.PERM_PROSUMER
newswarm = swarm.swarm.create(api, "newswarm", "DELETE ME",
        True, [res])
res_map = newswarm.getResources()
for res in res_map:
    print res
    print '    '+res_map[res].name+': '+str(res_map[res].permission)
swarms = swarm.getSwarms(api)
for swrm in swarms:
    print swrm.name
    for res in swrm.resources.values():
        print '    '+res.name+': '+str(res.permission)
#for res in swrm.resources.values():
#   print res.name+': '+str(res.permission)
#res = resource.getResources(api)[0]
#res.getSwarms()
res.destroy()
newswarm.destroy()
