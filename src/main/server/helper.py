import logging
import osmnx as ox
logging.basicConfig(level = logging.INFO)
'''This is a helper class which contains helper functions to make sure
    that can be used for performing different tasks.
    
'''

class helper:
    def __init__(self):
        self.location = None
    def validate_input(self, location: dict):
        '''This function validates the request body sent by client. A error message is passed to the client if request body
        doesn't follows specified format

        Args:
            location (dict): Client request body. Expected format : {
                        "source":"<required_field_str>, (<address, city, state>), (eg: 138 Brittany Manor Drive, Amherst, MA)",
                        "destination": "<required_field_str, (<address, city, state>), (1040 N Pleasant St, Amherst, MA)>",
                        "percentage_length":"<required_field_int, (should be >=100)>",
                        "max_min":"<required_field_str>, (min or max)",
                    }
        Returns:
            bool: True if valid, False otherwise
        
        '''
        self.location = location
        try:
            if ("source" not in self.location) or ("destination" not in self.location) or \
                ("percentage_length" not in self.location) or ("max_min" not in self.location):
                    return False
            source = self.location["source"]
            destination = self.location["destination"]
            percentage_length = self.location["percentage_length"]
            min_max = self.location["max_min"]

            if source == "" or destination == "" or min_max == "" or percentage_length == "":
                return False
            
            if (type(percentage_length)!=int or percentage_length<100) or type(source)!=str or type(destination)!=str or type(min_max)!=str:
                return False

            if not self.validate_address(self.location["source"]) or not self.validate_address(self.location["destination"]):
                return False


            return True
        except Exception as e:
            logging.info(f"Something went wrong while trying to validate input with exception {e}")

   
    def validate_location(self,graph, lat: float, long: float):
        '''This function checks if the location is valid. 
            Validating location means finding a valid node in the generated map which is at a distance of less than 1 km from 
            the given location.
        
        Args:
            graph (osmnx.graph): Generated graph of the source and destination city
            lat (float): location latitude
            long (float): location longitude

        Returns:
            osmnx.graph_node: nearest Valid node if the location is valid, None otherwise.
            bool: True if location is valid, False otherwise
        '''
        nearest_node, distance = ox.distance.nearest_nodes(graph, long, lat,return_dist=True)
        if distance > 10000:
            logging.error("Couldn't find a node within 1000 ms of the given location!!!")
            return nearest_node, False
        logging.info("Location is Valid!!!")
        return nearest_node, True

    def route_length(self, graph , path: list):
        '''Calculates the length of a given

        Args:
            graph (osmnx.graph): Generated graph of the source and destination city
            path (list[int]): A connected path in form of array of nodes from source to destination

        Returns:
            float: The length of the given path
        
        '''
        path_length = 0
        for idx in range(1,len(path)):
            
            path_length += graph.edges[path[idx-1], path[idx], 0]['length']
        return path_length

    def validate_address(self, address:str):
        '''Validates a given address to check if it follows the specified format <address, city, state>

        Args:
            address (str): Given address string


        Returns:
            bool: True if the address is in correct format False otherwise
        
        '''
        address_list = address.split(",")
        if len(address_list) <3:
            return False
        return True





