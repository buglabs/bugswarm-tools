import httplib
import json
import logging
import swarm

#TODO - better response code checking...
"""Implements resource object and helper functions"""
def getResources(apikey):
    """Retrieve a list of all resources associated with an api key

    @param apikey: an apikey object containing a valid configuration key

    @return: returns a list of all resource objects owned by the user.
    """
    conn = httplib.HTTPConnection(apikey.server)
    conn.request("GET", "/resources", None, {"x-bugswarmapikey":apikey.configuration})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    if resp.status >= 400:
        logging.warning('Resource list response: ('+str(resp.status)+'): '+txt)
    else:
        logging.debug('Resource list response: ('+str(resp.status)+'): '+txt)
    list = json.loads(txt)
    resources = []
    for item in list:
        res = resource(apikey, item["id"],
                       item["name"] if item.has_key("name") else False,
                       item["description"] if item.has_key("description") else False,
                       item["created_at"] if item.has_key("created_at") else False)
        resources.append(res)
    return resources

def getResourceByName(apikey, name):
    """Returns a resource object with a given name

    @param apikey: an apikey object containing a valid configuration key
    @param name: A short name for the resource

    @return: returns a resource object if found, None otherwise.
    """
    resources = getResources(apikey)
    for res in resources:
        if (res.name == name):
            return res
    return None

class resource:
    """Represents a resource, the fundamental agent in a BUGswarm application"""

    #Permission types
    PERM_NOT_SPECIFIED = -1
    PERM_NONE = 0
    PERM_CONSUMER = 1
    PERM_PRODUCER = 2
    PERM_PROSUMER = 3

    TYPE_PRODUCER = "producer"
    TYPE_CONSUMER = "consumer"

    def __init__(self, apikey, id, name=False, description=False, created_at=False, permission=PERM_NOT_SPECIFIED):
        """Create a resource object

        name and description are optional and can be retrieved by getInfo()

        @param apikey: an apikey object containing a valid configuration key
        @param id: the 40 character ID string of the resource
        @param name: A short name for the resource
        @param description: A longer description
        """

        self.apikey = apikey
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at
        self.permission = permission
        #if complete information was not given, try to retrieve it
        if not (name or description or created_at):
            self.getInfo()

    def getInfo(self):
        """Retrieve a resource's information from the swarm server"""
        conn = httplib.HTTPConnection(self.apikey.server)
        conn.request("GET", "/resources/%s"%(self.id), None,
                     {"x-bugswarmapikey":self.apikey.configuration})
        resp = conn.getresponse()
        txt = resp.read()
        conn.close()
        if resp.status >= 400:
            logging.warning('Resource info response: ('+str(resp.status)+'): '+txt)
        else:
            logging.debug('Resource info response: ('+str(resp.status)+'): '+txt)
        item = json.loads(txt)
        if (item.has_key("name")):
            self.name = item["name"]
        if (item.has_key("description")):
            self.description = item["description"]
        if (item.has_key("created_at")):
            self.created_at = item["created_at"]
        return self

    @classmethod
    def create(cls, apikey, name, description=None):
        """Create a new resource on the swarm server

        @param apikey: an apikey object containing a valid configuration
        @param name: A short name for the resource
        @param description: A longer description

        @return: Returns a new resource object
        """
        create_resource = {"name": name, "machine_type":"pc"}
        if description != None:
            create_resource["description"] = description
        create_resource_json = json.dumps(create_resource)
        conn = httplib.HTTPConnection(apikey.server)
        conn.request("POST", "/resources", create_resource_json,
                     {"x-bugswarmapikey":apikey.configuration})
        resp = conn.getresponse()
        txt = resp.read()
        if (resp.status >= 400):
            logging.error('Unable to create new resource '+name)
            return None
        logging.debug('Resource Create response: ('+str(resp.status)+'): '+txt)
        item = json.loads(txt)
        ret = cls(apikey, item["id"],
                       item["name"] if item.has_key("name") else False,
                       item["description"] if item.has_key("description") else False,
                       item["created_at"] if item.has_key("created_at") else False)
        return ret

    def update(self, name=None, description=None):
        """Update the resource information, informing the server of changes

        @param name: A short name for the resource
        @param description: A longer description

        @return: returns True if successful, False otherwise.
        """
        update_resource = {}
        if name != None:
            update_resource["name"] = name
        if description != None:
            update_resource["description"] = description
        update_resource_json = json.dumps(update_resource)
        conn = httplib.HTTPConnection(self.apikey.server)
        conn.request("PUT", "/resources/%s"%(self.id), update_resource_json,
                     {"x-bugswarmapikey":self.apikey.configuration})
        resp = conn.getresponse()
        txt = resp.read()
        conn.close()
        if (resp.status >= 400):
            logging.warning('Resource update response: ('+str(resp.status)+'): '+txt)
            return False
        logging.debug('Resource update response: ('+str(resp.status)+'): '+txt)
        if name != None:
            self.name = name
        if description != None:
            self.description = description
        return True

    def getSwarms(self):
        """Return a list of all swarms in which this resource can participate

        @return: returns a list of swarm objects.
        """
        conn = httplib.HTTPConnection(self.apikey.server)
        conn.request("GET", "/resources/%s/swarms"%(self.id), None,
                     {"x-bugswarmapikey":self.apikey.configuration})
        resp = conn.getresponse()
        txt = resp.read()
        conn.close()
        if resp.status >= 400:
            logging.warning('Resource swarms response: ('+str(resp.status)+'): '+txt)
        else:
            logging.debug('Resource swarms response: ('+str(resp.status)+'): '+txt)
        items = json.loads(txt)
        swarms = []
        for item in items:
            resources = {}
            if (item.has_key("resources")):
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
                    if not resources.has_key(res_data["resource_id"]):
                        resources[res_data["resource_id"]] = resource(self.apikey, res_data["resource_id"],
                            res_data["name"] if res_data.has_key("name") else False,
                            res_data["description"] if res_data.has_key("description") else False,
                            res_data["created_at"] if res_data.has_key("created_at") else False,
                            permission)
                    #if item is already in the resources map, logically OR it's permissions
                    else:
                        resources[res_data["resource_id"]].permission = resources[res_data["resource_id"]].permission | permission
            swrm = swarm.swarm(self.apikey, item["id"],
                item["name"] if item.has_key("name") else False,
                item["description"] if item.has_key("description") else False,
                item["created_at"] if item.has_key("created_at") else False,
                item["public"] if item.has_key("public") else False,
                resources)
            swarms.append(swrm)
        return swarms

    def destroy(self):
        """Remove this resource from BUGswarm

        @return: returns True if successful, False otherwise.
        """
        conn = httplib.HTTPConnection(self.apikey.server)
        conn.request("DELETE", "/resources/%s"%(self.id), None,
                     {"x-bugswarmapikey":self.apikey.configuration})
        resp = conn.getresponse()
        txt = resp.status
        conn.close()
        if str(txt) == "204":
            logging.debug('Resource Destroy response: ('+str(resp.status)+')')
            return True
        else:
            logging.warning('Resource Destroy response: ('+str(resp.status)+')')
            return False
