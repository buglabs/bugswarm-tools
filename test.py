#!/usr/bin/python
from BUGswarm import apikey
from BUGswarm import resource
from BUGswarm import swarm
import logging
import unittest

USERNAME = "atergis_dp"
PASSWORD = "buglabs"

class SwarmLibraryTest(unittest.TestCase):

    def setUp(self):
        self.api = apikey.apikey(USERNAME, PASSWORD)

    def test_resource(self):
        #Confirm we can create a resource
        test_resource = resource.resource.create(self.api,
                "DELETEMEname", "DELETEMEdesc")
        self.assertTrue(test_resource != None)
        self.assertTrue(resource.getResourceByName(self.api, "DELETEMEname") != None)
        #Confirm at least one resource is listed on the acct
        res_list = resource.getResources(self.api)
        self.assertTrue(len(res_list) > 0)
        #Double check that the server returns data on the created resource
        init_resource = resource.resource(self.api, test_resource.id)
        self.assertTrue(init_resource.name == "DELETEMEname")
        self.assertTrue(init_resource.description == "DELETEMEdesc")
        self.assertTrue(init_resource.created_at != None)
        self.assertTrue(init_resource.created_at != False)
        #Confirm we can actually update resource data
        self.assertTrue(test_resource.update("DELETEME", "DELETEMEnewdesc"))
        init_resource = resource.resource(self.api, test_resource.id)
        self.assertTrue(init_resource.name == "DELETEME")
        self.assertTrue(init_resource.description == "DELETEMEnewdesc")
        #Confirm we can destroy swarm objects
        self.assertTrue(test_resource.destroy())
        init_resource = resource.resource(self.api, test_resource.id)
        self.assertTrue(init_resource.name != "DELETEME")
        self.assertTrue(init_resource.description != "DELETEMEnewdesc")

    def test_swarm(self):
        #Create a resource for our testing
        test_resource = resource.resource.create(self.api,
                "DELETEMEname", "DELETEMEdesc")
        self.assertTrue(test_resource != None)
        self.assertTrue(resource.getResourceByName(self.api, "DELETEMEname") != None)
        test_resource.permission = resource.PERM_PROSUMER
        #Confirm we can create a swarm
        test_swarm = swarm.swarm.create(self.api, "DELETEME",
                "DELETEMEdesc", False, [test_resource])
        self.assertTrue(test_swarm != None)
        self.assertTrue(swarm.getSwarmByName(self.api,"DELETEMEname") != None)




if __name__ == '__main__':
    unittest.main()

logging.basicConfig(level=logging.DEBUG)
print "\n"
api = apikey.apikey("atergis_dp","buglabs")
oldres = resource.getResources(api)[0]
swarms = oldres.getSwarms()
for swrm in swarms:
    print swrm.name
    for res in swrm.resources:
        print '    '+swrm.resources[res].name

