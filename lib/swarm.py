import httplib
import json
import logging
from resource import resource

"""Implements Swarm object and helper functions"""
def getSwarms(apikey):
    """Retrieve a list of all swarms associated with this api key
    
    @param apikey: an apikey object containing a valid configuration key
    """
    
class swarm:
    """Represents a Swarm - a collection of linked resources"""

    def __init__(self, apikey, id, name=False, description=False, created_at=False, 
                public=False, resources=[]):
        """Initialize an existing resource and retrieve it's info
        
        @param apikey: an apikey object containing a valid configuration key
        @param id: if specified, this will retrieve resource details from swarm
                   otherwise, resource can be created using .create()
        """
        self.apikey = apikey
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at
        self.public = public
        self.resources = resources
        #if complete information was not given, try to retrieve it
        if not (name or description or created_at):
            self.getInfo()

    @classmethod
    def create(cls, name, description, public=False, resources={}):
        """Create a new swarm on the swarm server
        
        @param name: A short name for the swarm
        @param description: A longer description
        @param public: Boolean
        @param resources: An optional list of tuples in the format of
            (<resource>,<type>)
            where:
                Resource - a resource object
                Type - the type of resource EG
                    TYPE_PRODUCER
                    TYPE_CONSUMER
                    
        returns a swarm object 
        
        """

    def getInfo(self):
        """Retrieve a swarm's information from the swarm server"""
        conn = httplib.HTTPConnection(self.apikey.server)
        conn.request("GET", "/swarms/%s"%(self.id), None, 
                     {"x-bugswarmapikey":self.apikey.configuration})
        resp = conn.getresponse()
        txt = resp.read()
        conn.close()
        logging.debug('Swarm info response: ('+str(resp.status)+'): '+txt)
        item = json.loads(txt)
        if (item.has_key("name")):
            self.name = item["name"]
        if (item.has_key("description")):
            self.description = item["description"]
        if (item.has_key("created_at")):
            self.created_at = item["created_at"]
        if (item.has_key("public")):
            self.public = item["public"]
        if (item.has_key("resources")):
            self.resources = {}
            for res_data in item["resources"]:
                #retrieve resource_type and convert it into an enum'd permission
                permission = resource.PERM_NONE
                if res_data.has_key("resource_type"):
                    if (res_data["resource_type"] == resource.TYPE_PRODUCER):
                        permission = resource.PERM_PRODUCER
                    elif (res_data["resource_type"] == resource.TYPE_CONSUMER):
                        permission = resource.PERM_CONSUMER
                    else:
                        logging.warning('unknown resource_type '+str(item["resource_type"])+
                            ', assuming maximum permissions')
                        permission = resource.PERM_PROSUMER
                #If item is not already in the resources map, add it
                if not self.resources.has_key(res_data["resource_id"]):
                    self.resources[res_data["resource_id"]] = resource(self.apikey, res_data["resource_id"], 
                        res_data["name"] if res_data.has_key("name") else False,
                        res_data["description"] if res_data.has_key("description") else False,
                        res_data["created_at"] if res_data.has_key("created_at") else False,
                        permission)
                #if item is already in the resources map, logically OR it's permissions
                else:
                    self.resources[res_data["resource_id"]].permission = self.resources[res_data["resource_id"]].permission | permission
        return self

    def update(self, name, description, public):
        """Update the swarm information, informing the server of changes
        
        @param name: A short name for the swarm
        @param description: A longer description
        @param public: Boolean
        
        """
    def addResource(self, resource, type):
        """Add a resource to the swarm
        
        @param resource: a resource object
        @param type: the type of resource EG
                     TYPE_PRODUCER
                     TYPE_CONSUMER
        """
    def getResources(self, type=""):
        """Returns a list of all participant resources
        
        @param type: (optional) only return resources of a given type, EG
                     TYPE_PRODUCER
                     TYPE_CONSUMER
        """
    def removeResource(self, resource, type):
        """Add a resource from the
        
        @param resource: a resource object
        @param type: the type of resource EG
                     TYPE_PRODUCER
                     TYPE_CONSUMER
        """
    def destroy(self):
        """Remove this swarm from BUGswarm"""
