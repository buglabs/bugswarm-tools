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
    TYPE_BOTH = ""
    
    def __init__(self, username, password, server="api.bugswarm.net"):
        """Create a new apikey object, retrieving keys from the server
        
        @param username: A string, the account username
        @param password: A string, the account password
        @param server: A string containing the Swarm server, defaults to 
                       api.bugswarm.net
                       
        This will automatically retrieve keys from the server,
        generating new keys iff none have been generated.
         
        """
    
    @classmethod
    def useKeys(cls, configuration_key, participation_key, 
                server="api.bugswarm.net"):
        """Create a new apikey object from stored keys
        
        @param cls: the apikey class
        @param configuration_key: a 40-character string
        @param participation_key: a 40-character string
        @param server: A string containing the Swarm server, defaults to 
                       api.bugswarm.net
                       
        This helper classmethod will initialize an apikey object for you if
        the username and password are unavailable.
        
        NOTE - this object cannot be used for generating keys!
        
        """
            
    def generate(self, type=""):
        """Generate one or two new api keys
        
        @param type: a string specifying the key type.  See:
                     TYPE_CONFIGURATION
                     TYPE_PARTICIPATION
                     TYPE_BOTH (default)
        """
                
        