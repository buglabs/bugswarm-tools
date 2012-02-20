
"""Implements Swarm object and helper functions"""
def getSwarms(apikey):
    """Retrieve a list of all swarms associated with this api key
    
    @param apikey: an apikey object containing a valid configuration key
    """
    
class swarm:
    """Represents a Swarm - a collection of linked resources"""
    TYPE_PRODUCER = "producer"
    TYPE_CONSUMER = "consumer"
    def __init__(self, apikey, id):
        """Initialize an existing resource and retrieve it's info
        
        @param apikey: an apikey object containing a valid configuration key
        @param id: if specified, this will retrieve resource details from swarm
                   otherwise, resource can be created using .create()
        """
    @classmethod
    def create(cls, name, description, public=False, resources=[]):
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