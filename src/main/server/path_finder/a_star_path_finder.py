import heapq
import logging
from helper import helper
from path_finder.djikistra_path_finder import DjikstraPathFinder

'''

This class implements a modified version of Djikistra shortest path
algorithm to find a suitable path satisfiying percetange path length and 
elevation gain requirement of the client

'''
class AStarPathFinder():
    def __init__(self):
        self.djikstra = DjikstraPathFinder()
      

    # Our heuristic function is a simple eculedian distance between two points as we
    # know Eculidian distance between two points is the shortest distance between two points
    def heuristic_function(self,graph,start, end):
        return ((graph.nodes[start]['x']-graph.nodes[end]['x'])**2+(graph.nodes[start]['y']-graph.nodes[end]['y'])**2)**0.5
    
    def getNextNode(self,nodes, node_costs):
        return min(nodes, key = lambda item: sum(node_costs[item].values()))

    def get_coordinates(self,graph, path):
        coord = []
        for node in path:
            coord.append((graph.nodes[node]['y'], graph.nodes[node]['x']))
        return coord

    def get_path(self, graph, start, end, percentage_length, min_max_gain):
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

        # node_costs
        cost_martix = {} 
        cost_martix[start] = {}
        cost_martix[start]['g'] = 0
        cost_martix[start]['h'] = 0

        all_routes = []

        while begin:
            current = self.getNextNode(begin,cost_martix)
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
                    path_elevation = -1*elevation_gain if is_max else elevation_gain
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


        
    
