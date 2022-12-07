import logging
import osmnx as ox
logging.basicConfig(level = logging.INFO)
'''
This is a helper class which contains helper functions to make sure
that can be used for performing different tasks.

validate_input : This function is useful for validating the input data that is sent from client
It mainly performs empty string and data type validation as None type validation is done during parsing 
the request body.
'''
class helper:
    def __init__(self):
        self.location = None
    def validate_input(self, location):
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

            # if "algorithm" in location and (location["algorithm"]!="djikistra" or location["algorithm"]!="a*"):
            #     return False

            return True
        except Exception as e:
            logging.info(f"Something went wrong while trying to validate input with exception {e}")

    '''
    This function checks if the location is valid. 
    Validating location means finding a valid node in the generated map which is at a distance of less than 1 km from 
    the given location.
    '''
    def validate_location(self,graph, lat, long):
        nearest_node, distance = ox.distance.nearest_nodes(graph, long, lat,return_dist=True)
        if distance > 10000:
            logging.error("Couldn't find a node within 1000 ms of the given location!!!")
            return nearest_node, False
        logging.info("Location is Valid!!!")
        return nearest_node, True

    def route_length(self, graph , path):
        path_length = 0
        for idx in range(1,len(path)):
            
            path_length += graph.edges[path[idx-1], path[idx], 0]['length']
        return path_length

    def validate_address(self, address):
        address_list = address.split(",")
        if len(address_list) <3:
            return False
        return True

    def validate_algorithm(algorithm):
        if "djik" not in algorithm or "a*" not in algorithm:
            return False
        return True




