import pytest
import sys
sys.path.append("../..")

from helper import helper
from map_generator.generate_map import GenerateMap
from path_finder.djikistra_path_finder import DjikstraPathFinder

'''This file contains test suit for helper module

'''

@pytest.fixture
def helper_object():
    '''Returns and object of the helper class
    
    '''
    return helper()

@pytest.fixture
def correct_data():
    '''Returns a dummy well formatted request data that will be used for testing various functions of helper class
    
    '''
    return {
	"source":"138 Brittany Manor Drive, Amherst, MA",
	"destination": "115 Brittany Manor Drive, Amherst, MA",
	"percentage_length":100,
	"max_min":"min"
	
}

@pytest.fixture
def malformed_data():
    '''Returns a dummy malformed request data (percentage_length is string) that will be used for testing various functions of helper class
    
    '''
    return {
	"source":"138 Brittany Manor Drive, Amherst, MA",
	"destination": "115 Brittany Manor Drive, Amherst, MA",
	"percentage_length":"100",
	"max_min":"min"
	
}

@pytest.fixture
def generate_map_obj():
    return GenerateMap()


@pytest.fixture
def graph(generate_map_obj):
    '''Fetch the graph of Amherst, Mssachusetts. We will be using this graph for testing various functions inside helper

    
    '''
    map, _ = generate_map_obj.generateMap("Amherst", "MA")
    return map

@pytest.fixture
def lat_long_valid(generate_map_obj):
    '''Fetch the co-ordinates of a given address which is in the same city


    '''
   
    source_info = generate_map_obj.getLocationInfo("138 Brittany Manor Drive, Amherst, MA")
    return source_info["lat"], source_info["long"]

@pytest.fixture
def lat_long_invalid(generate_map_obj):
    '''Fetch the co-ordinates of a given address which is not in the given city


    '''

    source_info = generate_map_obj.getLocationInfo("19 MYRTLE ST, BOSTON, MA")
    return source_info["lat"], source_info["long"]

@pytest.fixture
def valid_address():
    '''A well formatted address
    
    '''
    return "138 Brittany Manor Drive, Amherst, MA"

@pytest.fixture
def invalid_address():
    '''A malformed address (city is missing)
    
    '''
    return "138 Brittany Manor Drive, MA"


@pytest.fixture
def get_path(graph,helper_object,generate_map_obj):
    '''A path from source node to destination node
    
    '''
    djikstra_path_finder = DjikstraPathFinder()
    src_address = "138 Brittany Manor Drive, Amherst, MA"
    dest_address = "115 Brittany Manor Drive, Amherst, MA"
    
    source_info = generate_map_obj.getLocationInfo(src_address)
    destination_info = generate_map_obj.getLocationInfo(dest_address)

    source_lat, source_long = source_info["lat"], source_info["long"]
    dest_lat, dest_long = destination_info["lat"], destination_info["long"]
    source_node,_ = helper_object.validate_location(graph, source_lat, source_long)
    dest_node,_ = helper_object.validate_location(graph, dest_lat, dest_long)

    path = djikstra_path_finder.get_shortest_path(graph, source_node,dest_node)

    return path

def test_validate_input_formatted_request_body(helper_object, correct_data):
    '''We are passing a well formated request body the assertion should pass if the function returns a valid boolean

    
    '''
    data = correct_data
    is_valid = helper_object.validate_input(data)
    assert is_valid == True

def test_validate_input_malformed_request_body(helper_object, malformed_data):
    '''We are passing a mal-formated request body (percentage_length_is_not_integer) the assertion should pass if the function returns a invalid boolean

    
    '''
    data = malformed_data
    is_valid = helper_object.validate_input(data)
    assert is_valid == False

def test_validate_location_valid_case(helper_object, graph,lat_long_valid):
    '''We are passing a valid location (i.e. there is a node in the range of 1000 mts from the given location) assertion should pass if
    the function returns a valid boolean
    
    '''
    lat, long = lat_long_valid
    _,is_valid = helper_object.validate_location(graph, lat, long)
    assert is_valid == True


def test_validate_location_invalid_case(helper_object, graph,lat_long_invalid):
    '''We are passing an invalid location (i.e. there is no node in the range of 1000 mts from the given location) assertion should pass if
    the function returns an invalid boolean
    
    '''
    lat, long = lat_long_invalid
    _,is_valid = helper_object.validate_location(graph, lat, long)
    assert is_valid == False

def test_validate_address_valid_case(helper_object, valid_address):
    '''We are testing our function against a valid well strutured address. Assertion should pass if function returns valid boolean
    
    '''

    is_valid = helper_object.validate_address(valid_address)
    assert is_valid == True

def test_validate_address_invalid_case(helper_object, invalid_address):
    '''We are testing our function against a malformed address. Assertion should pass if function returns invalid boolean
    
    '''

    is_valid = helper_object.validate_address(invalid_address)
    assert is_valid == False


def test_route_length(helper_object,graph, get_path):
    '''In this function we are fetching the length of the path and comparing it with the know result from Google maps. The assertion
    will pass if expected path length distance varies by 10 mts from actual path length
    
    '''
    actual_path_length = 125

    fetched_path_length = helper_object.route_length(graph, get_path)

    assert actual_path_length+10>=fetched_path_length>=actual_path_length-10



