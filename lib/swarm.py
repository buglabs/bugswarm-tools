import httplib
import json
import logging
import resource

"""Implements Swarm object and helper functions"""
def getSwarms(apikey):
    """Retrieve a list of all swarms associated with this api key

    @param apikey: an apikey object containing a valid configuration key

    @return: Returns a list containing all swarm objects owned by the user
    """
    conn = httplib.HTTPConnection(apikey.server)
    conn.request("GET", "/swarms", None,
                 {"x-bugswarmapikey":apikey.configuration})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    if resp.status >= 400:
        logging.debug('Swarm info response: ('+str(resp.status)+'): '+txt)
    else:
        logging.warning('Swarm info response: ('+str(resp.status)+'): '+txt)
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
                    resources[res_data["resource_id"]] = resource.resource(apikey, res_data["resource_id"],
                        res_data["name"] if res_data.has_key("name") else False,
                        res_data["description"] if res_data.has_key("description") else False,
                        res_data["created_at"] if res_data.has_key("created_at") else False,
                        permission)
                #if item is already in the resources map, logically OR it's permissions
                else:
                    resources[res_data["resource_id"]].permission = resources[res_data["resource_id"]].permission | permission
        swrm = swarm(apikey, item["id"],
            item["name"] if item.has_key("name") else False,
            item["description"] if item.has_key("description") else False,
            item["created_at"] if item.has_key("created_at") else False,
            item["public"] if item.has_key("public") else False,
            resources)
        swarms.append(swrm)
    return swarms

def getSwarmByName(apikey, name):
    """Returns a swarm object with a given name

    @param apikey: an apikey object containing a valid configuration key
    @param name: A short name for the resource

    @return: returns a swarm object if found, None otherwise.
    """
    swarms = getResources(apikey)
    for swrm in swarms:
        if (swrm.name == name):
            return swrm
    return None

class swarm:
    """Represents a Swarm - a collection of linked resources"""

    def __init__(self, apikey, id, name=False, description=False, created_at=False,
                public=False, resources=[]):
        """Initialize an existing resource and retrieve it's info

        @param apikey: an apikey object containing a valid configuration key
        @param id: the id of the swarm object.  If unknown, use the create
            classmethod
        @param name: (optional) A text name for the swarm
        @param description: (optional) A text description for the swarm
        @param created_at: (optional) The date and time of object creation, eg
            "2011-08-29T20:17:08.676Z"
        @param public: (optional) Whether or not this is a public swarm, boolean
            (default: False)
        @param resources: (optional) A list of resource objects  that are a
            member of this swarm.
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
    def create(cls, apikey, name, description, public=False, resources=[]):
        """Create a new swarm on the swarm server

        @param name: A short name for the swarm
        @param description: A longer description
        @param public: Boolean
        @param resources: An optional dict of resource objects, keyed by id

        @return: returns a new swarm object
        """
        res_list = []
        for res in resources:
            #lookup the resource string
            if res.permission == resource.PERM_CONSUMER:
                res_list.append({"resource_id": res.id,
                    "resource_type": resource.TYPE_CONSUMER})
            elif res.permission == resource.PERM_PRODUCER:
                res_list.append({"resource_id": res.id,
                    "resource_type": resource.TYPE_PPRODUCER})
            elif res.permission == resource.PERM_PROSUMER:
                res_list.append({"resource_id": res.id,
                    "resource_type": resource.TYPE_CONSUMER})
                res_list.append({"resource_id": res.id,
                    "resource_type": resource.TYPE_PRODUCER})
        create_obj = {"name": name, "description": description,
                "public": public, "resources": res_list}
        create_swarm_json = json.dumps(create_obj)
        conn = httplib.HTTPConnection(apikey.server)
        conn.request("POST", "/swarms",create_swarm_json,
                     {"x-bugswarmapikey":apikey.configuration})
        resp = conn.getresponse()
        txt = resp.read()
        conn.close()
        if (resp.status >= 400):
            logging.error('Unable to create new swarm '+name)
            return None
        logging.debug('Swarm info response: ('+str(resp.status)+'): '+txt)
        item = json.loads(txt)
        ret = cls(apikey, item["id"],
                item["name"] if item.has_key("name") else False,
                item["description"] if item.has_key("description") else False)
        return ret

    def getInfo(self):
        """Retrieve a swarm's information from the swarm server"""
        conn = httplib.HTTPConnection(self.apikey.server)
        conn.request("GET", "/swarms/%s"%(self.id), None,
                     {"x-bugswarmapikey":self.apikey.configuration})
        resp = conn.getresponse()
        txt = resp.read()
        conn.close()
        if resp.status >= 400:
            logging.warning('Swarm info response: ('+str(resp.status)+'): '+txt)
        else:
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
                    self.resources[res_data["resource_id"]] = resource.resource(self.apikey, res_data["resource_id"],
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

        @param name: (optional) A short name for the swarm
        @param description: (optional) A longer description
        @param public: (optional) Boolean

        @return: True if success, False otherwise.
        """
        update_swarm = {}
        if name != None:
            update_swarm["name"] = name
        if description != None:
            update_swarm["description"] = description
        if public != None:
            update_swarm["public"] = public
        update_swarm_json = json.dumps(update_swarm)
        conn = httplib.HTTPConnection(self.apikey.server)
        conn.request("PUT", "/swarms/%s"%(self.id), update_swarm_json,
                     {"x-bugswarmapikey":self.apikey.configuration})
        resp = conn.getresponse()
        txt = resp.read()
        conn.close()
        if resp.status >= 400:
            logging.warning('Swarm info response: ('+str(resp.status)+'): '+txt)
            return False
        logging.debug('Swarm info response: ('+str(resp.status)+'): '+txt)
        if name != None:
            self.name = name
        if description != None:
            self.description = description
        if public != None:
            self.public = public
        return True

    def addResource(self, resource):
        """Add a resource to the swarm

        Make sure to specify the .permission var of the resource before adding.

        @param resource: a resource object

        @return: True if success, False otherwise.
        """
        add_resource = {"resource_id": resource.id}
        if resource.permission == resource.PERM_PRODUCER or resource.permission == resource.PERM_PROSUMER:
            add_resource["resource_type"] = resource.TYPE_PRODUCER
        elif resource.permission == resource.PERM_CONSUMER:
            add_resource["resource_type"] = resource.TYPE_CONSUMER
        add_resource_json = json.dumps(add_resource)
        conn = httplib.HTTPConnection(self.apikey.server)
        conn.request("PUT", "/swarms/%s/resources"%(self.id), add_resource_json,
                     {"x-bugswarmapikey":self.apikey.configuration})
        resp = conn.getresponse()
        txt = resp.read()
        conn.close()
        if txt != "Created":
            logging.warning('Swarm add_resource response: ('+str(resp.status)+'): '+txt)
            return False
        logging.debug('Swarm add_resource response: ('+str(resp.status)+'): '+txt)
        if resource.permission == resource.PERM_PROSUMER:
            add_resource["resource_type"] = resource.TYPE_CONSUMER
            add_resource_json = json.dumps(add_resource)
            conn = httplib.HTTPConnection(self.apikey.server)
            conn.request("PUT", "/swarms/%s/resources"%(self.id), add_resource_json,
                         {"x-bugswarmapikey":self.apikey.configuration})
            resp = conn.getresponse()
            txt = resp.read()
            conn.close()
            if txt != "Created":
                logging.warning('Swarm add_resource response: ('+str(resp.status)+'): '+txt)
                return False
            logging.debug('Swarm add_resource response: ('+str(resp.status)+'): '+txt)
        self.getInfo()
        return True

    def getResources(self, resource_type=None):
        """Returns a list of all participant resources

        @param resource_type: (optional) only return resources of a given type, EG
                     TYPE_PRODUCER
                     TYPE_CONSUMER

        @return: returns a dict of resources, indexed by resource_id
        """
        conn = httplib.HTTPConnection(self.apikey.server)
        if resource_type != None:
            conn.request("GET", "/swarms/%s/resources?type=%s"%(self.id,resource_type),
                    None, {"x-bugswarmapikey":self.apikey.configuration})
        else:
            conn.request("GET", "/swarms/%s/resources"%(self.id), None,
                     {"x-bugswarmapikey":self.apikey.configuration})
        resp = conn.getresponse()
        txt = resp.read()
        conn.close()
        if resp.status >= 400:
            logging.warning('Swarm get_resource response: ('+str(resp.status)+'): '+txt)
        else:
            logging.debug('Swarm get_resource response: ('+str(resp.status)+'): '+txt)
        res_list = {}
        item = json.loads(txt)
        for res_data in item:
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
            if not res_list.has_key(res_data["resource_id"]):
                res_list[res_data["resource_id"]] = resource.resource(self.apikey, res_data["resource_id"],
                    res_data["name"] if res_data.has_key("name") else False,
                    res_data["description"] if res_data.has_key("description") else False,
                    res_data["created_at"] if res_data.has_key("created_at") else False,
                    permission)
            #if item is already in the resources map, logically OR it's permissions
            else:
                res_list[res_data["resource_id"]].permission = res_list[res_data["resource_id"]].permission | permission
        return res_list

    def removeResource(self, resource):
        """Add a resource from the

        @param resource: a resource object

        @return: returns True if successful, False otherwise.
        """
        delete_resource = {"resource_id": resource.id}
        if resource.permission == resource.PERM_PRODUCER or resource.permission == resource.PERM_PROSUMER:
            delete_resource["resource_type"] = resource.TYPE_PRODUCER
        elif resource.permission == resource.PERM_CONSUMER:
            delete_resource["resource_type"] = resource.TYPE_CONSUMER
        delete_resource_json = json.dumps(delete_resource)
        conn = httplib.HTTPConnection(self.apikey.server)
        conn.request("DELETE", "/swarms/%s/resources"%(self.id), delete_resource_json,
                     {"x-bugswarmapikey":self.apikey.configuration})
        resp = conn.getresponse()
        txt = resp.read()
        conn.close()
        if resp.status >= 400:
            logging.warning('Swarm delete_resource response: ('+str(resp.status)+'): '+txt)
        else:
            logging.debug('Swarm delete_resource response: ('+str(resp.status)+'): '+txt)
        if txt != "":
            return False
        if resource.permission == resource.PERM_PROSUMER:
            delete_resource["resource_type"] = resource.TYPE_CONSUMER
            delete_resource_json = json.dumps(add_resource)
            conn = httplib.HTTPConnection(self.apikey.server)
            conn.request("DELETE", "/swarms/%s/resources"%(self.id),
                    delete_resource_json,
                    {"x-bugswarmapikey":self.apikey.configuration})
            resp = conn.getresponse()
            txt = resp.read()
            conn.close()
            if resp.status >= 400:
                logging.warning('Swarm delete_resource response: ('+str(resp.status)+'): '+txt)
            else:
                logging.debug('Swarm delete_resource response: ('+str(resp.status)+'): '+txt)
            if txt != "":
                return False
        self.getInfo()
        return True

    def destroy(self):
        """Remove this swarm from BUGswarm

        @return: returns True if successful, False otherwise.
        """
        conn = httplib.HTTPConnection(self.apikey.server)
        conn.request("DELETE", "/swarms/%s"%(self.id), None,
                     {"x-bugswarmapikey":self.apikey.configuration})
        resp = conn.getresponse()
        txt = resp.read()
        conn.close()
        if resp.status == 204:
            logging.debug('Swarm destroy response: ('+str(resp.status)+')')
            return True
        else:
            logging.warning('Swarm destroy response: ('+str(resp.status)+')')
            return False
