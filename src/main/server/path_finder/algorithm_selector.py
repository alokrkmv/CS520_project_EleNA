from path_finder.djikistra_path_finder import DjikstraPathFinder
from path_finder.a_star_path_finder import AStarPathFinder
class AlgorithmSelector:
    def __init__(self):
        self.djikstra = DjikstraPathFinder()
        self.a_star = AStarPathFinder()
    def pick_algorithm(self,graph, nearest_node_source, nearest_node_destination, percentage_length, max_min):
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