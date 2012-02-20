
"""Implements resource object and helper functions"""
def getResources(apikey):
    """Retrieve a list of all resources associated with an api key
    
    @param apikey: an apikey object containing a valid configuration key
    """
    
class resource:
    """Represents a resource, the fundamental agent in a BUGswarm application"""
    def __init__(self, apikey, id):
        """Initialize an existing resource and retrieve it's info
        
        @param apikey: an apikey object containing a valid configuration key
        @param id: if specified, this will retrieve resource details from swarm
                   otherwise, resource can be created using .create()
                   
        """
        self.apikey = apikey
        self.id = id
        
    @classmethod
    def create(cls, name, description):
        """Create a new resource on the swarm server
        
        @param name: A short name for the resource
        @param description: A longer description
        
        Returns a new resource object
        """
    
    def update(self, name, description):
        """Update the resource information, informing the server of changes
        
        @param name: A short name for the resource
        @param description: A longer description
        """
    def getSwarms(self):
        """Return a list of all swarms in which this resource can participate"""
    def destroy(self):
        """Remove this resource from BUGswarm"""