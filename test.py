from lib import apikey
from lib import resource
import logging

logging.basicConfig(level=logging.DEBUG)
api = apikey.apikey("atergis_dp","buglabs")
res = resource.getResources(api)[0]
res.getSwarms()
res = resource.resource.create(api,"pythontest01","DELETE ME")
res.update("pythonsauce","DELETEMEMOAR")
res.destroy()
