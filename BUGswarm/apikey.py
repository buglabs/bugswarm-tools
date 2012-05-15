import httplib
import base64
import json
import logging

"""Implements apikey object"""

class apikey:
    """Represents a set of API keys for the BUGSwarm platform.

    Required by all other swarm API methods.

    """
    TYPE_CONFIGURATION = "configuration"
    TYPE_PARTICIPATION = "participation"
    TYPE_BOTH = None

    def __init__(self, username=False, password=False, server="api.bugswarm.net"):
        """Create a new apikey object, retrieving keys from the server

        Username and Password may be omitted if keys are directly initialized

        @param username: A string, the account username
        @param password: A string, the account password
        @param server: A string containing the Swarm server, defaults to
                       api.bugswarm.net
        """
        self.server = server
        self.username = username
        self.password = password
        self.configuration = False
        self.participation = False
        if (username and password):
            self.getKeys(username, password);

    def getKeys(self, username, password):
        """Retrieve keys from the server

        @param username: A string, the account username
        @param password: A string, the account password
        """
        self.username = username
        self.password = password
        conn = httplib.HTTPConnection(self.server)
        auth_hash = username + ":" + password
        auth_header = "Basic " + base64.b64encode(auth_hash)
        logging.debug('Getting API keys with auth_header: '+auth_header)
        conn.request("GET", "/keys", None, {"Authorization":auth_header})
        resp = conn.getresponse()
        txt = resp.read()
        logging.debug('API key response: ('+str(resp.status)+'): '+txt)
        if resp.status >= 400:
            logging.error('Bad response retrieving API Keys: ('+str(resp.status)+'): '+txt)
            return
        keys = json.loads(txt)
        for key in keys:
            if (key["type"] == "configuration"):
                self.configuration = key["key"]
            if (key["type"] == "participation"):
                self.participation = key["key"]
        logging.debug('Retrieved keys: c('+self.configuration+') p('+self.participation+')')

    @classmethod
    def useKeys(cls, configuration_key, participation_key,
                server="api.bugswarm.net"):
        """Create a new apikey object from stored keys

        This helper classmethod will initialize an apikey object for you if
        the username and password are unavailable.

        NOTE - this object cannot be used for generating keys!

        @param cls: the apikey class
        @param configuration_key: a 40-character string
        @param participation_key: a 40-character string
        @param server: A string containing the Swarm server, defaults to
                       api.bugswarm.net

        @return: returns a new apikey object
        """
        ret = cls(server)
        ret.configuration = configuration_key
        ret.participation = participation_key
        return ret

    def generate(self, key_type=None):
        """Generate one or two new api keys

        @param key_type: a string specifying the key type.  See:
                     TYPE_CONFIGURATION
                     TYPE_PARTICIPATION
                     TYPE_BOTH (default)

        @return: returns True if successful, False otherwise.
        """
        if (not(self.username and self.password)):
            logging.error("Cannot generate API keys - "+
                          "Username and password not specified")
            return False
        conn = httplib.HTTPConnection(self.server)
        auth_hash = self.username + ":" + self.password
        auth_header = "Basic " + base64.b64encode(auth_hash)
        if (key_type != None):
            conn.request("POST", "/keys/" + key_type, None, {"Authorization":auth_header})
        else:
            conn.request("POST", "/keys", None, {"Authorization":auth_header})
        resp = conn.getresponse()
        txt = resp.read()
        conn.close()
        logging.debug('API key response: ('+str(resp.status)+'): '+txt)
        if resp.status >= 400:
            logging.error('Bad response retrieving API Keys: ('+str(resp.status)+'): '+txt)
            return False
        keys = json.loads(txt)
        for key in keys:
            if (key["type"] == "configuration"):
                self.configuration = key["key"]
            if (key["type"] == "participation"):
                self.participation = key["key"]
        logging.debug('Retrieved keys: c('+self.configuration+') p('+self.participation+')')
        return True

