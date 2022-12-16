import logging
import math
import time
import requests
import pandas as pd
import numpy as np
import networkx as nx
import pickle as pkl
import osmnx as ox
import os
import googlemaps

from geopy.geocoders import Nominatim

from osmnx import downloader
from osmnx import utils
logging.basicConfig(level = logging.INFO)
class GenerateMap:

    '''This class is responsible for generating the map of city in which source and destination lies. It also saves the generated map into the
        cache in case of cache miss and serves the map from cache in case of case hit
    
    '''
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent = "project_elena")
        self.city = None
        self.state = None
        self.file_path = f"generated_maps/{self.city}_{self.state}.pkl"
        self.image_path = None
        pass
    
    '''
        Using the osmnx graph plotter to generate the plot of the graph
    '''
    def generateGraphPlot(self, graph):
        '''This function plots the map using osmnx default graph plotter and saves it as a jpg image
        
        Args:
            graph (osmnx.graph): The map to be plotted

        '''
        ox.log('Generating graph based on elevation !')
        ox.plot_graph(G=graph, figsize=(40, 40), bgcolor = "#FFFFFF",node_color='b', node_size=5, edge_color='#0000FF', edge_linewidth=1,save=True, filepath=self.image_path,show=False)

   
    def getLocationInfo(self, location : str):
        '''This method fetches city, state and lat-long info for a particular address. City and state is fetched by parsing the address data
            while latitude and longitude is fetched using geopy library.
        Args:
            location (str): Address for which location data needs to be fetched

        Return:
            dict: A dictionary consisting {"lat":<latitude <str>>,
                                           "long":<longitude <str>>,
                                           "city":<str>,
                                           "state":<str>}
        '''
        try:
            location_info = location.split(",")
            params = {}
           
   

            gmaps = googlemaps.Client(key='AIzaSyBVdyePhhYFnn5-jJP5jCaO4NBuR_c_ADE')

            geocode_result = gmaps.geocode(location)
            params["lat"] =  geocode_result[0]["geometry"]["location"]["lat"]
            params["long"] = geocode_result[0]["geometry"]["location"]["lng"]
            params["city"] = location_info[-3].strip()
            params["state"] = location_info[-2].strip()
            return params
        except Exception as e:
            logging.exception(f"Something went wrong in fetching location info for given location")
            return params
            
    
   
    def generateMap(self, city, state):
        '''This method generates map of the city and state with elevation info attached to each node
            For getting the elevation info we are using open elevation API which is free version of Google's elevation API
            For generating the map we wil be using osmnx map generator.

            Args:
                city(str): City
                state(str): State

        '''
        self.city = city
        self.state = state
        self.file_path = f"generated_maps/{self.city}_{self.state}.pkl"
        self.image_path = f"generated_maps/{self.city}_{self.state}.png"

        # If the map is already present in the cache then serve from cache
        if os.path.exists(self.file_path):
            logging.info(f"The Graph for city {city} and state {state} is served from cache")
            graph = None
            try:
                graph = pkl.load(open(self.file_path,"rb"))
                try:
                    logging.info(f"Plotting the graph for city {city} state {state}")
                    # self.generateGraphPlot(graph)
                except Exception as e:
                    logging.warning(f"Graph generated successfuly however plotting failed!!! Aborting plot generation!!!")
                finally:
                    print(graph)
                    return graph, True
            except Exception as e:
                logging.error(f"Something went wrong while trying to load the graph with error {e}")
                return graph, False
        try:
            params = {}
            params['city']  = city
            params['state'] = state
            params['country'] = 'USA'

            # Generate the city state map using osmnx map generator if the graph is not already present in the cache
            graph = ox.graph_from_place(params, network_type='bike')
            # Adding elevation data
            graph = self.add_node_elevations_open(graph)
            
            #Add grade attribute to each graph edge.
            #Vectorized function to calculate the directed grade (ie, rise over run) for each edge in the graph and add it to the edge as an attribute. 
            #Nodes must already have elevation attributes to use this function.
            
            graph = ox.add_edge_grades(graph)
            try:
                logging.info(f"Adding the generated graph for city {city} state {state} in cache")
                pkl.dump(graph, open(self.file_path, "wb"))
            except Exception as e:
                logging.warning(f"Caching the graph failed with error {e}!!")
            finally:
                try:
                    # self.generateGraphPlot(graph)
                    pass
                except Exception as e:
                    logging.warning(f"Graph generated successfuly however plotting failed!!! Aborting plot generation!!!")
                finally:
                    return graph, True
        except Exception as e:
            logging.exception(f"Unable to generate Map for city {city} and state {state} from osmnx with error {e}")

            return graph, False

   
    def add_node_elevations_open(self, G, max_locations_per_batch=180,
                             pause_duration=0.02, precision=3):  # pragma: no cover

        '''Osmnx provides method get_node_elevation_google which attaches elevation data to each node of the generated graph
            using Google's elevation API. Although Google's elevation API is not free, hence here we have modified this
            function to use open-elevation API which is an open source version of Google's elevation API.
        '''

        """
        Add `elevation` (meters) attribute to each node using a web service.
        This uses the Open Elevation API and hence doesn't require any API key.
        See also the `add_edge_grades` function.
        Parameters
        ----------
        G : networkx.MultiDiGraph
            input graph
        api_key : string
            a Google Maps Elevation API key
        max_locations_per_batch : int
            max number of coordinate pairs to submit in each API call (if this is
            too high, the server will reject the request because its character
            limit exceeds the max allowed)
        pause_duration : float
            time to pause between API calls, which can be increased if you get
            rate limited
        precision : int
            decimal precision to round elevation values
        Returns
        -------
        G : networkx.MultiDiGraph
            graph with node elevation attributes
        """

        url_template = 'https://api.open-elevation.com/api/v1/lookup?locations={}'

        node_points = pd.Series(
        {node: f'{data["y"]:.5f},{data["x"]:.5f}' for node, data in G.nodes(data=True)}
        )
        n_calls = int(np.ceil(len(node_points) / max_locations_per_batch))
        utils.log(f"Requesting node elevations from the API in {n_calls} calls")

        # break the series of coordinates into chunks of size max_locations_per_batch
        # API format is locations=lat,lng|lat,lng|lat,lng|lat,lng...
        results = []
        for i in range(0, len(node_points), max_locations_per_batch):
            chunk = node_points.iloc[i : i + max_locations_per_batch]
            locations = "|".join(chunk)
            url = url_template.format(locations)

            # check if this request is already in the cache (if global use_cache=True)
            cached_response_json = downloader._retrieve_from_cache(url)
            if cached_response_json is not None:
                response_json = cached_response_json
            else:
                try:
                    # request the elevations from the API
                    utils.log(f"Requesting node elevations: {url}")
                    time.sleep(pause_duration)
                    response = requests.get(url)
                    response_json = response.json()
                    downloader._save_to_cache(url, response_json, response.status_code)
                except Exception as e:
                    utils.log(e)
                    utils.log(f"Server responded with {response.status_code}: {response.reason}")

            # append these elevation results to the list of all results
            results.extend(response_json["results"])

        # sanity check that all our vectors have the same number of elements
        if not (len(results) == len(G) == len(node_points)):
            raise Exception(
                f"Graph has {len(G)} nodes but we received {len(results)} results from elevation API"
            )
        else:
            utils.log(
                f"Graph has {len(G)} nodes and we received {len(results)} results from elevation API"
            )

        # add elevation as an attribute to the nodes
        df = pd.DataFrame(node_points, columns=["node_points"])
        df["elevation"] = [result["elevation"] for result in results]
        df["elevation"] = df["elevation"].round(precision)
        nx.set_node_attributes(G, name="elevation", values=df["elevation"].to_dict())
        utils.log("Added elevation data from Google to all nodes.")

        return G






    
