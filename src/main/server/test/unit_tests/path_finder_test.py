import pytest
import sys

import math
sys.path.append("../..")

from map_generator.generate_map import GenerateMap
from path_finder.djikistra_path_finder import DjikstraPathFinder
from helper import helper


'''This file contains test suit for map generator module

'''

from map_generator.generate_map import GenerateMap
from path_finder.djikistra_path_finder import DjikstraPathFinder

@pytest.fixture
def generate_map_obj():
    '''Returns an object of the map generator class
    
    '''

    return GenerateMap()

@pytest.fixture
def path_finder_object():
    '''Returns an object of the pathfinder class
    
    '''
    return DjikstraPathFinder()

@pytest.fixture
def helper_object():
    '''Returns an object of the helper class
    
    '''
    return helper()
@pytest.fixture
def graph(generate_map_obj):
    '''Fetch the graph of Amherst, Mssachusetts. We will be using this graph for testing various functions inside helper

    
    '''
    map, _ = generate_map_obj.generateMap("Amherst", "MA")
    return map

@pytest.fixture
def src_address():
    '''Fetch the graph of Amherst, Mssachusetts. We will be using this graph for testing various functions inside helper

    
    '''
    return "138 Brittany Manor Drive, Amherst, MA"

@pytest.fixture
def dest_address():
    '''Fetch the graph of Amherst, Mssachusetts. We will be using this graph for testing various functions inside helper

    
    '''
    return "115 Brittany Manor Drive, Amherst, MA"

@pytest.fixture
def destination_address_for_elevation():
    '''Fetch the graph of Amherst, Mssachusetts. We will be using this graph for testing various functions inside helper

    
    '''
    return "96 N Pleasant St, Amherst, MA"




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
def graph():
    '''Fetch the graph of Amherst, Mssachusetts. We will be using this graph for testing various functions inside helper

    
    '''
    generate_map_obj = GenerateMap()
    map, _ = generate_map_obj.generateMap("Amherst", "MA")
    return map

@pytest.fixture
def lat_long_valid():
    '''Fetch the co-ordinates of a given address which is in the same city


    '''
    generate_map_obj = GenerateMap()
    source_info = generate_map_obj.getLocationInfo("138 Brittany Manor Drive, Amherst, MA")
    return source_info["lat"], source_info["long"]



@pytest.fixture
def get_path(graph,helper_object,generate_map_obj,path_finder_object,src_address, dest_address):
    '''A path from source node to destination node
    
    '''
    generate_map_obj = GenerateMap()
    source_info = generate_map_obj.getLocationInfo(src_address)
    destination_info = generate_map_obj.getLocationInfo(dest_address)

    source_lat, source_long = source_info["lat"], source_info["long"]
    dest_lat, dest_long = destination_info["lat"], destination_info["long"]
    source_node,_ = helper_object.validate_location(graph, source_lat, source_long)
    dest_node,_ = helper_object.validate_location(graph, dest_lat, dest_long)

    path = path_finder_object.get_shortest_path(graph, source_node,dest_node)

    return path


@pytest.fixture
def get_path_for_elevation(graph,helper_object,generate_map_obj,path_finder_object,src_address, destination_address_for_elevation):
    '''A path from source node to destination node
    
    '''
    generate_map_obj = GenerateMap()
    source_info = generate_map_obj.getLocationInfo(src_address)
    destination_info = generate_map_obj.getLocationInfo(destination_address_for_elevation)

    source_lat, source_long = source_info["lat"], source_info["long"]
    dest_lat, dest_long = destination_info["lat"], destination_info["long"]
    source_node,_ = helper_object.validate_location(graph, source_lat, source_long)
    dest_node,_ = helper_object.validate_location(graph, dest_lat, dest_long)

    path = path_finder_object.get_shortest_path(graph, source_node,dest_node)

    return path

@pytest.fixture
def get_source_dest_node(generate_map_obj,helper_object,graph):
    src_address = "138 Brittany Manor Drive, Amherst, MA"
    dest_address = "248 Amherst Rd, Sunderland, MA"
    source_info = generate_map_obj.getLocationInfo(src_address)
    destination_info = generate_map_obj.getLocationInfo(dest_address)
    source_lat, source_long = source_info["lat"], source_info["long"]
    dest_lat, dest_long = destination_info["lat"], destination_info["long"]
    source_node,_ = helper_object.validate_location(graph, source_lat, source_long)
    dest_node,_ = helper_object.validate_location(graph, dest_lat, dest_long)

    return source_node,dest_node


def test_get_path_length(get_path,graph,path_finder_object):
    '''Here we are testing for length of shortest path from source to destination and asserting it against the known length from Google maps.
    Assertion will return true if the fetched path length is in range of 10 mts of actual_path length
    
    '''
    actual_path_length = 250

    fetched_path_length = path_finder_object.get_path_length(graph,get_path)

    assert actual_path_length+10>=fetched_path_length>=actual_path_length-10

def test_net_elevation_gain(get_path_for_elevation,graph,path_finder_object):
    '''Here we are testing for net elevation calculation for a path and asserting it against the known elevation data from Google elevation API.
    Assertion will return true if elevation gain is in 5 mts of actual elevation gain
    
    '''
    actual_elevation_gain = 54

    fetched_elevation_gain = path_finder_object.get_net_elevations(graph,get_path_for_elevation)

    assert actual_elevation_gain+10>=fetched_elevation_gain>=actual_elevation_gain-10


def test_shortest_path_for_nodes(get_path):
    '''Here we are testing for number of nodes in the shortest path and assering it against know value from Google maps API
    
    '''
    actual_number_of_nodes = 7


    assert actual_number_of_nodes == len(get_path)

def test_shortest_path_for_length(graph,get_path, path_finder_object):
    '''Here we are testing for length of shortest path and assering it against know value from Google maps API
    
    '''

    actual_path_length = 253

    fetched_path_length = path_finder_object.get_path_length(graph,get_path)

    assert actual_path_length+10>=fetched_path_length>=actual_path_length-10

def test_get_path_djikistra(graph, path_finder_object,get_source_dest_node):
    '''Here we are testing for recommended path langth and elevation and testing it against know value from Google maps API and google
    elevation API
    
    '''

    actual_elevation_gain = 96

    actual_path_length = 9180

    nearest_node_source, nearest_node_destination = get_source_dest_node

    _, fetched_path_length, fetched_elevation_gain = path_finder_object.get_path(graph, nearest_node_source, nearest_node_destination, 110, "min" )
    

    

    assert actual_path_length+10>=fetched_path_length>=actual_path_length-10
    assert actual_elevation_gain+10>=fetched_elevation_gain>=actual_elevation_gain-10

def test_min_max_elevation(graph, path_finder_object,get_source_dest_node):
    '''Here we are testing if our path finding algorithm is taking min_max choice of elevation into account. Assertion will pass only if
    elevation for max choice greater than or equal to that for min choice for same path length
    
    '''



    nearest_node_source, nearest_node_destination = get_source_dest_node

    _, _, fetched_elevation_gain_min = path_finder_object.get_path(graph, nearest_node_source, nearest_node_destination, 110, "min" )
    
    _, _, fetched_elevation_gain_max = path_finder_object.get_path(graph, nearest_node_source, nearest_node_destination, 110, "max" )

    assert (fetched_elevation_gain_max>=fetched_elevation_gain_min) == True

def test_percentage_path_length(graph, path_finder_object,get_source_dest_node):
    '''Here we are testing if length of path generated is taking percentage path length choice of user into account or not. Assertion will pass only if
    path length for higher percentage is greater than or equal to for that of lower percentage for same elevation gain choice
    
    '''



    nearest_node_source, nearest_node_destination = get_source_dest_node

    _, path_length_min, _ = path_finder_object.get_path(graph, nearest_node_source, nearest_node_destination, 100, "min" )
    
    _, path_length_max, _ = path_finder_object.get_path(graph, nearest_node_source, nearest_node_destination, 110, "min" )

    assert (path_length_max>=path_length_min) == True
    

   




