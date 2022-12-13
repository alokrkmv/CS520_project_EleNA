import heapq
import logging
from helper import helper
from path_finder.djikistra_path_finder import DjikstraPathFinder
from path_finder.path_finder import PathFinderInterface


'''

This class implements a modified version of Astar shortest path
algorithm to find a suitable path satisfiying percetange path length and 
elevation gain requirement of the client

'''
class AStarPathFinder(PathFinderInterface):
    '''This class implements a modified version of Astar shortest path
        algorithm to find a suitable path satisfiying percetange path length and 
        elevation gain requirement of the client

    '''
    def __init__(self):
        self.djikstra = DjikstraPathFinder()
      

    def heuristic_function(self,graph,start, end):
        '''As A* is a heuristic based path finder algorithm we need to have a heuristic function. This is a simple heuristic
            function which finds shortest possible distance (Eculedian distance) between source and destination

        Args:
            graph (osmnx.graph): The graph of the city in which source and destination lies
            start (osmnx.graph.node): First Node
            end (osmnx.graph.node): Second Node

        Returns:
            float: Eculidian distance between two nodes

        '''
        return ((graph.nodes[start]['x']-graph.nodes[end]['x'])**2+(graph.nodes[start]['y']-graph.nodes[end]['y'])**2)**0.5
    
    def find_next_node(self,nodes, node_costs):
        '''This function finds the next node with mimimum cost from the current node

        Args:
            nodes (list[node]): An array of nodes
            node_cost (dict): Cost metrix

        Returns:
            osmnx.graph.node: Returns the next node with minimum cost

        '''
        min_cost = float("inf")
        next_node = None
        for node in nodes:
            cost = sum(node_costs[node].values())
            if cost < min_cost:
                min_cost = cost
                next_node = node
        return next_node

    def get_coordinates(self,graph, path):
        '''This function finds x and y coordinates for each node in the path

        Args:
            graph (osmnx.graph): The graph of the city in which source and destination lies
            path list[node]: A list of nodes from source to destination representing the path from source to destination

        Returns:
            coord: Returns an array of tuples where each tuple corresponds to x and y co-ordinate of the corrsponding path node

        '''
        coord = []
        for node in path:
            coord.append((graph.nodes[node]['y'], graph.nodes[node]['x']))
        return coord

    def get_path(self, graph, start, end, percentage_length, min_max_gain):

        '''This function returns most optimal path between a given source and destination node for a given input paramater
            We are using a modified version of A* to find the most optimal path for given source and destination combination 
            considering user's preference for elevation gain and maximum path length.
            Distance from one node to another is the edge weight
        
        Args:
            graph (osmnx.graph): The graph of the city in which source and destination lies
            start (osmnx.graph.node): Source node
            end (osmnx.graph.node): Destination node
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
        # get the shortest path
        min_distance = self.djikstra.get_path_length(graph, self.djikstra.get_shortest_path(graph, start, end))

        begin = set()
        terminate = set()

        begin.add(start)

        parent = {}
        parent[start] = None

        cost_martix = {} 
        cost_martix[start] = {}
        cost_martix[start]['g'] = 0
        cost_martix[start]['h'] = 0

        all_routes = []

        while begin:
            current = self.find_next_node(begin,cost_martix)
            begin.remove(current)
            if current == end:
                if cost_martix[current]['g'] <= (percentage_length*min_distance)/100:
                    path = []
                    path_temp = current
                    while path_temp is not None:
                        path.append(path_temp)
                        path_temp = parent[path_temp]
                    path = path[::-1]

                    elevation_gain = self.djikstra.get_net_elevations(graph, path)
                    path_elevation = elevation_gain
                    if is_max:
                        path_elevation = -1*elevation_gain

                    path_length = self.djikstra.get_path_length(graph, path)
                    coordinates = self.get_coordinates(graph, path)
                    heapq.heappush(all_routes, (path_elevation, path_length, coordinates))

                    cost_martix[current]['g'] = float('inf')
                else:
                    break
            else:
                terminate.add(current)
                for neigbhor in graph[current]:
                    if neigbhor in terminate:
                        continue
                    if neigbhor in begin:
                        old_cost = cost_martix[neigbhor]['g']
                        new_cost = cost_martix[current]['g']+graph.edges[current, neigbhor, 0]['length']
                        if old_cost>new_cost:
                            cost_martix[neigbhor]['g'] = new_cost
                            parent[neigbhor] = current

                    else:
                        g_cost = cost_martix[current]['g']+graph.edges[current, neigbhor, 0]['length']
                        h_cost = self.heuristic_function(graph, current, end)

                        parent[neigbhor] = current
                        cost_martix[neigbhor] = {}
                        cost_martix[neigbhor]['g'] = g_cost
                        cost_martix[neigbhor]['h'] = h_cost
                        begin.add(neigbhor)

        if all_routes:
            path_elevation, path_length, path_details = heapq.heappop(all_routes)
            if is_max: 
                path_elevation *= -1
            return path_details, path_length, path_elevation
        return None


        
    
