from path_finder.djikistra_path_finder import DjikstraPathFinder
from path_finder.a_star_path_finder import AStarPathFinder


class AlgorithmSelector:
    '''This class implements a function responsible for picking the between a_star and Djikistra algorithm for generating final result

    '''
    def __init__(self):
        self.djikstra = DjikstraPathFinder()
        self.a_star = AStarPathFinder()
    def pick_algorithm(self,graph, nearest_node_source, nearest_node_destination, percentage_length, max_min):
        '''This function takes a graph(map of the city), start_node, end_node, percentage path length, 
           max or min elevation gain and fetches most optimal path from both Djikistra and A_star path finding algorithm. 
           Then fetches the final result taking into client's choice of elevation gain

        Args:
            graph (osmnx.graph): The graph of the city in which source and destination lies
            nearest_node_source (osmnx.graph.node): Source node nearest to the given source
            nearest_node_destination (osmnx.graph.node): Destination node nearest to the given destination
            percentage_length (int): Maximum percentage length above the shortest path length user is willing to go
            min_max (str): User's choice of minimizing or maximizing elevation gain. max means user intends to maximize elevation gain
                                min means user wants to minimize elevation gain

        Returns:
            list[list[float]]: An array of lat, long pairs denoting the most optimizing path based on user's input
            float: length of the path
            float: elevation gain across the path

        '''
        # Get details from Djikstra
        route_1, dist_1, elevation_gain_1 = self.djikstra.get_path(graph, nearest_node_source, nearest_node_destination, percentage_length, max_min )
        # Get details from Astar
        route_2, dist_2, elevation_gain_2 = self.a_star.get_path(graph, nearest_node_source, nearest_node_destination, percentage_length, max_min )

        is_max = True if max_min == "max" else False
        if is_max:
            if elevation_gain_1>=elevation_gain_2:
                return route_1, dist_1, elevation_gain_1 
            else:
                return route_2, dist_2, elevation_gain_2
        else:
            if elevation_gain_1<=elevation_gain_2:
                return route_1, dist_1, elevation_gain_1
            else:
                return route_2, dist_2, elevation_gain_2