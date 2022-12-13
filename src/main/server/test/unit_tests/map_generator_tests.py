import pytest
import sys

import math
sys.path.append("../..")


'''This file contains test suit for map generator module

'''

from map_generator.generate_map import GenerateMap

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
def address():
    '''Fetch the graph of Amherst, Mssachusetts. We will be using this graph for testing various functions inside helper

    
    '''
    return "138 Brittany Manor Drive, Amherst, MA"

def test_graph_for_edges(graph):
    '''Test if the generated graph has correct number of edges. Assertion will pass if number of edges in the generated graph is within
    50 of source of truth fetched from Google maps api
    
    '''

    actual_number_of_edges = 10614
    generated_number_of_edges = graph.number_of_edges()
    assert actual_number_of_edges+50>=generated_number_of_edges>=actual_number_of_edges-50

def test_graph_for_nodes(graph):
    '''Test if the generated graph has correct number of nodes. Assertion will pass if number of nodes in the generated graph is within
    50 of source of truth fetched from Google maps api
    
    '''

    actual_number_of_edges = 4219
    generated_number_of_edges = graph.number_of_nodes()
    assert actual_number_of_edges+50>=generated_number_of_edges>=actual_number_of_edges-50

def test_location_info(generate_map_obj, address):
    '''Test if the generated co-ordinates of the address are correct. Assertion will pass if generated co-ordinates are equal to the source of
    truth from google map


    '''
    params = generate_map_obj.getLocationInfo(address)
    generated_lat = round(params["lat"], 4)
    generated_long = round(params["long"], 4)
    actual_lat = 42.3494
    actual_long = -72.5284
    # As we are comparing float values we will compare for some degree of precision rather than exact value
    assert math.isclose(generated_lat, actual_lat, abs_tol=0.0005) == True
    assert math.isclose(generated_long, actual_long, abs_tol=0.0005) == True


    
