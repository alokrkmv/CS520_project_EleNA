import json
from flask import Flask, request
from helper import helper
import ast
import logging
from map_generator.generate_map import GenerateMap
from path_finder.algorithm_selector import AlgorithmSelector
from flask_cors import CORS
logging.basicConfig(level = logging.INFO)
app = Flask(__name__)
CORS(app)

'''
Sample Request body : 

"data":{
	"source":"138 Brittany Manor Drive, Amherst, MA",
	"destination": "Amherst Commons, Amherst, MA",
	"percentage_length":"100",
	"max_min":"min",
    "algorithm":"dijkstra"
	
}

Sample response:

"response":{
    'Route' : route,
    'Distance':dist,
    'Elevation Gain':elevation
}
'''
@app.route("/fetch_route",methods=["POST"])
def fetch_route():
    try:
        req_data = request.json
        data_dict = None
        if type(req_data)==dict:
            data_dict = req_data.get("data")
        else:
            data_dict = ast.literal_eval(req_data)

        

        # data_dict = data.get("data")
        # data_dict = data
        data_dict["percentage_length"] = int(data_dict["percentage_length"])
        if data_dict == None:
            return {"message":"Empty request body"}
        helper_obj = helper()
        # Validating the inpute for required fields
        try:
            if not helper_obj.validate_input(data_dict):
                response_dict = {
                    "message":"Invalid input!!! Make sure that the request body is valid",
                    "valid_request_body_template":{
                        "source":"<required_field_str>, (<address, city, state>), (eg: 138 Brittany Manor Drive, Amherst, MA)",
                        "destination": "<required_field_str, (<address, city, state>), (1040 N Pleasant St, Amherst, MA)>",
                        "percentage_length":"<required_field_int, (should be >=100)>",
                        "max_min":"<required_field_str>, (min or max)",
                        "algorithm":"<optional_field_str>, (djikistra or a*)"
                    }
                }
                return response_dict
        except Exception as e:
            logging.exception(f"Something went wrong in validationg input with exception {e}")
            return {"message":f"Something went wrong in validating input with exception {e}"}
        source = data_dict["source"]
        destination = data_dict["destination"]
        max_min = data_dict["max_min"]
        percentage_length = data_dict["percentage_length"]
        algorithm = data_dict.get("algorithm", None)
        map_generator_obj = GenerateMap()
        source_info = map_generator_obj.getLocationInfo(source)
        if source_info == None or "lat" not in source_info or "long" not in source_info or "city" not in source_info \
            or "state" not in source_info:
            logging.ERROR(f"Unable to fetch location info for address {source}")
            return {"message":f"Unable to fetch location info for address {source}"}
        destination_info = map_generator_obj.getLocationInfo(destination)
        if destination_info == None or "lat" not in destination_info or "long" not in destination_info or "city" not in destination_info \
            or "state" not in destination_info:
            logging.ERROR(f"Unable to fetch location info for address {destination}")
            return {"message":f"Unable to fetch location info for address {destination}"}

    
    except Exception as e:
        logging.exception(f"Something went wrong in parsing data with error {e}")
        return {"message":f"Something went wrong in parsing data with error {e}"}

    # Generating the map for city and state

    graph, is_generated = map_generator_obj.generateMap(source_info["city"], source_info["state"])
    
    if not is_generated:
        logging.error(f"Something went wrong while trying to fetch map for city {source_info['city']} and {source_info['state']}")
        return {"message":f"Something went wrong while trying to fetch map for city {source_info['city']} and {source_info['state']}"}


    nearest_node_source, is_source_valid = helper_obj.validate_location(graph, source_info["lat"],source_info["long"])
    if not is_source_valid:
        logging.exception("Invalid source location. Please try again with different address!!!")
        return {"message":"Invalid source location. Please try again with different address!!!"}
    nearest_node_destination, is_destination_valid = helper_obj.validate_location(graph, destination_info["lat"],destination_info["long"])
    if not is_destination_valid:
        logging.exception("Invalid destination location. Please try again with different address!!!")
        return {"message":"Invalid destination location. Please try again with different address!!!"}

    
    route = None
    dist = None
    elevation_gain = None
    # Default algorithm for path finding is djikistra
    if algorithm == None or "dji" in algorithm:
        algorithm_selector = AlgorithmSelector()
        route, dist, elevation_gain = algorithm_selector.pick_algorithm(graph, nearest_node_source, nearest_node_destination, percentage_length, max_min )
        if route == None or dist == None or elevation_gain == None:
            logging.error("Something went wrong while trying to fetch required metrices for the given input")
            return {"message":"Something went wrong while trying to fetch required metrices for the given input!!! please try with a different input"}
        res = {
            "route":route,
            "distance": f"{dist:.3f} mts",
            "elevation_gain": f"{elevation_gain:.3f} mts",
            "source":[source_info["lat"],source_info["long"]],
            "destination":[destination_info["lat"],destination_info["long"]]

        }
        print(res)
        return res
    else:
        pass
            
    
    

    return {"graph":True}
    
    # return data.get("data")
if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)