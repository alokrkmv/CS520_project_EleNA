import heapq
import logging
from helper import helper
from path_finder.path_finder import PathFinderInterface
import math

class DjikstraPathFinder(PathFinderInterface):
    '''This class implements a modified version of Djikistra shortest path
        algorithm to find a suitable path satisfiying percetange path length and 
        elevation gain requirement of the client

    '''
    def __init__(self):
        pass

   
    def generate_path_array(self, reverse_path, start_node, end_node):
        '''Generated path from a key-value pair parent child dict for a given source and destination node

        Args:
            reverse_path(dict[node]:node): A key value pair dict with key as child node and value as parent node
            start_node(osmnx.graph.node): Source Node
            end_node(osmnx.graph.node): Destination Node

        Returns:
            list[(float,float)]: A list of tuple reprsenting co-ordinates of each node of the generated path

        '''
        path = []
        path.append(end_node)
        while end_node!=start_node:
            temp = reverse_path[end_node]
            path.append(temp)
            end_node = temp
        return path[::-1]
    
    def get_coordinates(self,graph, path):
        '''This functions fetches x and y co-ordinates for each node of the path

        Args:
            graph (osmnx.graph): The graph of the city in which source and destination lies
            path list[node]: A list of nodes from source to destination representing the path from source to destination
        
        Returns:
            list[(float,float)]: A list of tuple reprsenting co-ordinates of each node of the path
        
        '''
        coord = []
        for node in path:
            coord.append((graph.nodes[node]['y'], graph.nodes[node]['x']))
        return coord

    def clean_coordinates(self,coord):
        if len(coord) <= 25:
            return coord
        coord_len = len(coord)
        print(coord)

        new_coords = []

        step = math.ceil(coord_len/23)
        for i in range(0, coord_len - 1, step):
            new_coords.append(coord[i])

        new_coords.append(coord[coord_len - 1])
        print(len(new_coords))
        return new_coords
        
    
    def get_path_length(self, graph , path):
        '''This function calculates the path length of a given path

        Args:
            graph (osmnx.graph): The graph of the city in which source and destination lies
            path list[node]: A list of nodes from source to destination representing the path from source to destination

        Returns:
            float: Length of the entire path.
        
        '''
        path_length = 0
      
        for idx in range(1,len(path)):
            graph.edges[path[idx-1], path[idx], 0]['length']
            path_length += graph.edges[path[idx-1], path[idx], 0]['length']
        return path_length

    
    
    def get_elevation_gain(self, graph, start_node, end_node):
        '''This function calculates elevation gain between two nodes

        Args:
            graph (osmnx.graph): The graph of the city in which source and destination lies
            start_node (osmnx.graph.node): First Node
            end_node (osmnx.graph.node): Second Node

        Returns:
            float: The elevation gain between the two given nodes
        '''
        if start_node == end_node:
            return 0
        return graph.nodes[start_node]['elevation'] - graph.nodes[end_node]['elevation']
    
    def get_net_elevations(self, graph, path):
        '''This function calculates net elevation gain from source to destination while traversing a given path

        Args:
            graph (osmnx.graph): The graph of the city in which source and destination lies
            path list[node]: A list of nodes from source to destination representing the path from source to destination

        Returns:
            float: The net elevation gain that can be achieved while traversing the given path 
        '''
        elevation = 0
        for idx in range(len(path)-1):
            curr_elevation = self.get_elevation_gain(graph, path[idx], path[idx+1])
            elevation += curr_elevation if curr_elevation > 0 else 0 
        return elevation

    def get_shortest_path(self,graph, start_node, end_node):
        '''This function returns shortest path between a given source and destination node
            We are using Djikistra algorithm to find shortest path between two nodes.
            Distance from one node to another is the edge weight
        
        Args:
            graph (osmnx.graph): The graph of the city in which source and destination lies
            start_node (osmnx.graph.node): Source node
            end_node (osmnx.graph.node): Destination node

        Returns:
            list[nodes]: A list of nodes from source to destination represting the shortest possible path from source to destination

        '''
        heap = []
        heapq.heapify(heap)
        # Start node will have a weight of zero
        heapq.heappush(heap, (0,start_node))
        path = {}
        weights = {}
        path[start_node] = None
        weights[start_node] = 0
        while len(heap)>0:
            curr_cost, curr_node = heapq.heappop(heap)
            # We have found the path no need to traverse further
            if curr_node == end_node:
                break

            for _,next_node,_ in graph.edges(curr_node, data=True):
                curr_cost+=graph.edges[curr_node, next_node, 0]['length']
                if next_node not in weights or curr_cost<weights[next_node]:
                    weights[next_node] = curr_cost
                    heapq.heappush(heap,(curr_cost,next_node))
                    path[next_node] = curr_node
                
        

        return self.generate_path_array(path, start_node, end_node)


    def get_path(self, graph,start_node, end_node, percentage_length, min_max_gain):
        '''This function takes a graph(map of the city), start_node, end_node, percentage path length, 
           max or min elevation gain and returns path(an array of nodes from source to destination)
           elevation gain, path length

        Args:
            graph (osmnx.graph): The graph of the city in which source and destination lies
            start_node (osmnx.graph.node): Source node
            end_node (osmnx.graph.node): Destination node
            percentage_length (int): Maximum percentage length above the shortest path length user is willing to go
            min_max_gain (str): User's choice of minimizing or maximizing elevation gain. max means user intends to maximize elevation gain
            min means user wants to minimize elevation gain

        Returns:
            list[list[float]]: An array of lat, long pairs denoting the most optimizing path based on user's input
            float: length of the path
            float: elevation gain across the path

        '''
        is_max = False
        if min_max_gain == "max":
            is_max = True
        helper_obj = helper()
        
        min_distance = helper_obj.route_length(graph, self.get_shortest_path(graph, start_node, end_node))
        all_path = {}

        for _ in range(100, int(percentage_length)+1,5):
            weights = {}
            elevations = {}
            weights[start_node] = 0
            elevations[start_node] = 0
            heap = []
            heapq.heappush(heap,(0, start_node))
            path = {}
            path[start_node] = None
            while heap:
                elevation,curr_node = heapq.heappop(heap)
                if curr_node == end_node:
                    if weights.get(curr_node,0)<= (percentage_length*min_distance)/100:
                        break
                for _,next_node,_ in graph.edges(curr_node, data=True):
                    new_cost = weights.get(curr_node,0) + graph.edges[curr_node, next_node, 0]['length']
                    curr_elveation = elevations.get(curr_node,0)
                    elevation_cost = self.get_elevation_gain(graph, curr_node, next_node)
                    
                    if elevation_cost >0:
                        curr_elveation += elevation_cost
                        
                    if next_node not in weights or  new_cost < weights[next_node] :
                        weights[next_node] = new_cost
                        elevations[next_node] = curr_elveation
                        
                        if is_max:
                            heapq.heappush(heap,(-1*curr_elveation, next_node))
                        else:
                            heapq.heappush(heap,(curr_elveation, next_node))
                        path[next_node] = curr_node
            generated_path = self.generate_path_array(path, start_node, end_node)
            all_path[self.get_net_elevations(graph, generated_path)] = generated_path
        
        min_elevation = float('inf')
        max_elevation = float('-inf')
        
        
        for path in all_path.keys():
            min_elevation = min(min_elevation, path)
            max_elevation = max(max_elevation, path)
        
        
        final_path = None
        if is_max:
            final_path = all_path[max_elevation]
        else:
            final_path = all_path[min_elevation]
            
            

        gat_path_lat_long = self.clean_coordinates(self.get_coordinates(graph, final_path))
        get_path_length = self.get_path_length(graph, final_path)
        get_path_elevation = self.get_net_elevations(graph, final_path)
        
        return gat_path_lat_long, get_path_length, get_path_elevation
        

    

        
        
