import osmnx as ox
import networkx as nx

import numpy as np

from heapq import *
import matplotlib.pyplot as plt
from collections import deque, defaultdict

import time

class ElevationAlgorithms:

    def __init__(self, G, percentage = 0.0, is_max = True):
        """
        Class Initializer
        Parameters:
        G : Graph project
        percentage : percentage over the shortest_distance
        is_max : True for maximize elevation, False for minimize elevation
        """
        self.G = G
        self.is_max = is_max
        self.percentage = percentage
        self.optimal_path = [[], 0.0, float('-inf'), 0.0]
        self.source_node, self.destination_node = None, None


    def verify_valid_nodes(self):
        """
        Verify if the source node and destination node are valid or not i.e.None
        """
        if self.source_node is None or self.destination_node is None:
            return False
        return True

    def astar(self):
        """
        Find the nodes in the optimal path with heuristic using A* algorithm
        """
        self.add_distance_from_destination(self.G, self.destination_node)

        if not self.verify_valid_nodes() : return
        G, shortest_distance = self.G, self.shortest_distance
        percentage, is_max = self.percentage, self.is_max
        source_node, destination_node = self.source_node, self.destination_node

        closed_set = set()

        open_set = set()
        open_set.add(source_node)

        last_node = {}

        g_score = {}
        for node in G.nodes():
            g_score[node] = float("inf")

        g_score[source_node] = 0

        g_score1 = {}
        for node in G.nodes():
            g_score1[node] = float("inf")

        g_score1[source_node] = 0

        f_score = {}

        f_score[source_node] = G.nodes[source_node]['distance_from_destination']

        while len(open_set):
            current_node = min([(node,f_score[node]) for node in open_set], key=lambda t: t[1])[0]
            if current_node == destination_node:
                  if not last_node or not current_node : return
                  total_path = [current_node]
                  while current_node in last_node:
                      current_node = last_node[current_node]
                      total_path.append(current_node)
                  self.optimal_path = [total_path[:], self.compute_elevation(total_path, "normal"), self.compute_elevation(total_path, "gain"), \
                                                                                  self.compute_elevation(total_path, "drop")]
                  return

            open_set.remove(current_node)
            closed_set.add(current_node)
            for neighbor in G.neighbors(current_node):
                if neighbor in closed_set:
                    continue 

                approx_g_score = g_score[current_node] + self.node_cost(current_node, neighbor, "gain")
                approx_g_score1 = g_score1[current_node] + self.node_cost(current_node, neighbor, "normal")
                if neighbor not in open_set and approx_g_score1<=(1+percentage)*shortest_distance:
                    open_set.add(neighbor)
                else:
                    if approx_g_score >= g_score[neighbor] or approx_g_score1>=(1+percentage)*shortest_distance:
                        continue 
                last_node[neighbor] = current_node
                g_score[neighbor] = approx_g_score
                g_score1[neighbor] = approx_g_score1
                f_score[neighbor] = g_score[neighbor] + G.nodes[neighbor]['distance_from_destination']


    def node_cost(self, node1, node2, cost_type = "normal"):
        """
        Cost between two nodes based on the cost_type
        Parameters:
        node1: 1st node
        node2 : 2nd node
        cost_type : cost type between the nodes
        Return:
        Cost chosen between node1 and node2
        """
        G = self.G

        if node1 is None or node2 is None : return
        
        if cost_type == "normal":
            try : return G.edges[node1, node2 ,0]["length"]
            except : return G.edges[node1, node2]["weight"]
        
        elif cost_type == "gain":
            return max(0.0, G.nodes[node2]["elevation"] - G.nodes[node1]["elevation"])

        elif cost_type == "final-elevation":
            return G.nodes[node2]["elevation"] - G.nodes[node1]["elevation"]
        
        elif cost_type == "drop":
            return max(0.0, G.nodes[node1]["elevation"] - G.nodes[node2]["elevation"])
        
        else:
            return abs(G.nodes[node1]["elevation"] - G.nodes[node2]["elevation"])

    
    def compute_elevation(self, path, cost_type = "final-elevation", piece_wise = False):
        """
        Compute the cost of the route for given list of node id
        Parameters :
        path : node ids list
        cost_type : cost between the two nodes
        piece_wise : boolean variable to indicate piece_wise cost between node to be returned
        Return :
        total cost for the path or piecewise cost
        """
        total_elevation = 0
        
        if piece_wise : piece_wise_elevations = []
        
        for i in range(len(path)-1):

            if cost_type == "final-elevation":
                elevation_difference = self.node_cost(path[i], path[i+1], "final-elevation")
            
            elif cost_type == "gain":
                elevation_difference = self.node_cost(path[i],path[i+1],"gain")
            
            elif cost_type == "drop":
                elevation_difference = self.node_cost(path[i],path[i+1],"drop")
            
            elif cost_type == "normal":
                elevation_difference = self.node_cost(path[i],path[i+1],"normal")
            
            total_elevation = total_elevation + elevation_difference
            
            if piece_wise : piece_wise_elevations.append(node_cost)
        
        if piece_wise:
            return total_elevation, piece_wise_elevations
        
        else:
            return total_elevation


    def get_path(self, parent, destination):
        "Function to get path between parent and destination"
        route = [destination]
        
        current = parent[destination]
        
        while current != -1:
            route.append(current)
            current = parent[current]
        
        return route[::-1]


    def dijkstra(self, edge_value):
        """
        Find the path between source node and destination node which maximizes/minimize elevation
        Params:
        edge_value : list of two items
        Return:
        priority of target node in heap,distance covered to reach target node and a dictionary mapping parent
        and children
        """
        if not self.verify_valid_nodes():
            return
        
        G, percentage, shortest_distance, is_max = self.G, self.percentage, self.shortest_distance, self.is_max
        source_node = self.source_node 
        destination_node = self.destination_node
        queue = [(0.0, 0.0, source_node)]
        visited_nodes = set()
        minimum_distances = {source_node: 0}

        parent_dict = defaultdict(int)
        parent_dict[source_node] = -1

        while len(queue) != 0:

            current_priority, current_distance, current_node = heappop(queue)

            if current_node not in visited_nodes:
                
                visited_nodes.add(current_node)

                if current_node == destination_node:
                    return current_priority, current_distance, parent_dict

                for neighbors in G.neighbors(current_node):

                    if neighbors in visited_nodes: continue
                    
                    previous = minimum_distances.get(neighbors, None)
                    elevation_diff = self.node_cost(current_node, neighbors, "normal")

                    if is_max :
                        if edge_value[0] == 1:
                            next_elevation_diff = elevation_diff - self.node_cost(current_node, neighbors, "final-elevation")
                        elif edge_value[0] == 2:
                            next_elevation_diff = (elevation_diff - self.node_cost(current_node, neighbors, "final-elevation"))*elevation_diff
                        elif edge_value[0] == 3:
                            next_elevation_diff = elevation_diff + self.node_cost(current_node, neighbors, "drop")
                    else:
                        if edge_value[0] == 1:
                            next_elevation_diff = elevation_diff + self.node_cost(current_node, neighbors, "final-elevation")
                        elif edge_value[0] == 2:
                            next_elevation_diff = (elevation_diff + self.node_cost(current_node, neighbors, "final-elevation"))*elevation_diff
                        else:
                            next_elevation_diff = elevation_diff + self.node_cost(current_node, neighbors, "gain")
                    
                    if edge_value[1]:
                         next_elevation_diff = next_elevation_diff + current_priority
                    
                    next_distance = current_distance + elevation_diff
                    if next_distance <= shortest_distance*(1.0+percentage) and (previous is None or next_elevation_diff < previous):
                        parent_dict[neighbors] = current_node
                        minimum_distances[neighbors] = next_elevation_diff
                        heappush(queue, (next_elevation_diff, next_distance, neighbors))

        return None, None, None


    def dijkstra_all_paths(self):
    
        "chose the best path by trying path with different cost-type"

        if not self.verify_valid_nodes():
            return
        source_node, destination_node = self.source_node, self.destination_node
        for edge_value in [[1, True], [2, True], [3, True], [1, False], [2, False], [3, False]]:
            _, current_distance, parent_dict = self.dijkstra(edge_value)

            if not current_distance : continue

            path = self.get_path(parent_dict, destination_node)

            elevation_distance = self.compute_elevation(path, "gain")
            drop_distance = self.compute_elevation(path, "drop")

            if self.is_max :
                if (elevation_distance > self.optimal_path[2]) or (elevation_distance == self.optimal_path[2] and current_distance < self.optimal_path[1]):
                    self.optimal_path = [path[:], current_distance, elevation_distance, drop_distance]
            else:
                if (elevation_distance < self.optimal_path[2]) or (elevation_distance == self.optimal_path[2] and current_distance < self.optimal_path[1]):
                    self.optimal_path = [path[:], current_distance,  elevation_distance, drop_distance]

        return

    def distance_between_coordinates(self, source_latitude, source_longitude, destination_latitude, destination_longitude):
        """
        Return the distance between source and destination
        Parameters:
        source_latitude : latitude of source node
        source_longitude : longitude of source node
        destination_latitude : latitude of destination node
        destination_longitude : longitude of destination node
        Return:
        distance between source and destination node
        """
        earth_radius=6371008.8 #radius of the earth
        
        source_latitude = np.radians(source_latitude)
        source_longitude = np.radians(source_longitude)
        destination_latitude = np.radians(destination_latitude)
        destination_longitude = np.radians(destination_longitude)

        longitude_difference = destination_longitude - source_longitude
        latitude_difference = destination_latitude - source_latitude

        arc = np.sin(latitude_difference / 2)**2 + np.cos(source_latitude) * np.cos(destination_latitude) * np.sin(longitude_difference / 2)**2
        curvature = 2 * np.arctan2(np.sqrt(arc), np.sqrt(1 - arc))

        return earth_radius * curvature

    def add_distance_from_destination(self, G, destination):
        """
        Add distance from destination to a node
        Parameters:
        G : graph of Amherst
        destination : destination node
        Return:
        Updated graph G
        """

        destination_node = G.nodes[destination]
        destination_latitude = destination_node["y"]
        destination_longitude = destination_node["x"]
        
        for node, data in G.nodes(data=True):
            node_latitude = G.nodes[node]['y']
            node_longitude = G.nodes[node]['x']
            distance = self.distance_between_coordinates(destination_latitude, destination_longitude, node_latitude, node_longitude)            
            data['distance_from_destination'] = distance
            
        return G


    def calculate_shortest_path(self, start_location, end_location, percentage, algorithm, is_max):
        """
        Function to calculate the shortest path between start location and end location
        Parameters:
        start_location : metadata for start_location i.e.tuple(latitude, longitude)
        end_location : metadata for end_location i.e. tuple(latitude, longitude)
        percentage : percent by which we can go above minimum distance
        algorithm : algorithm used for finding the optimal path
        is_max : True for maximize elevation, False for minimize elevation
        Return:
        two lists containing best route, distance between the start node and end node in best route,
        positive change and negative change in elevation
        1st list is for shortest path, 2nd for path with elevation
        """

        G = self.G
        self.percentage = percentage/100.0
        self.is_max = is_max
        self.source_node, self.destination_node = None, None

        if is_max  : self.optimal_path = [[], 0.0, float('-inf'), float('-inf')]
        else : self.optimal_path = [[], 0.0, float('inf'), float('-inf')]

        self.source_node, distance1 = ox.get_nearest_node(G, point = start_location, return_dist = True)
        self.destination_node, distance2 = ox.get_nearest_node(G, point = end_location, return_dist = True)
        
        if distance1 > 1000 or distance2 > 1000:
            print("Invalid input")
            return None, None

        self.shortest_route = nx.shortest_path(G, source = self.source_node, target = self.destination_node, weight='length')
        self.shortest_distance  = sum(ox.utils_graph.get_route_edge_attributes(G, self.shortest_route, 'length'))


        if algorithm == "astar":
            print("Astar algorithm is being used to calculate path with elevation.")
            astar_start_time = time.time()
            self.astar()
            astar_end_time = time.time()

            print("A* time of execution: ", astar_end_time - astar_start_time)

            with open("empirical_analysis/astar_time.txt", 'a+') as f:
                f.write(str(astar_end_time - astar_start_time) + "\n")
            
            if len(self.optimal_path[0]) == 0 :
                self.djikstra_all_paths()

        else :
            print("Dijkstra algorithm is being used to calculate path with elevation.")
            dijkstra_start_time = time.time()
            self.dijkstra_all_paths()
            dijkstra_end_time = time.time()

            print("Dijkstra time of execution: ", dijkstra_end_time - dijkstra_start_time)

            with open("empirical_analysis/dijkstra_time.txt", 'a+') as f:
                f.write(str(dijkstra_end_time - dijkstra_start_time) + "\n")

        shortest_route_coordinates = [[G.nodes[node]['x'],G.nodes[node]['y']] for node in self.shortest_route]
        shortest_route_metadata = [shortest_route_coordinates, self.shortest_distance, \
                            self.compute_elevation(self.shortest_route, "gain"), self.compute_elevation(self.shortest_route, "drop")]

        if (self.is_max  and self.optimal_path[2] == float('-inf')) or (not self.is_max and self.optimal_path[3] == float('-inf')):
            return shortest_route_metadata, [[], 0.0, 0, 0]

        self.optimal_path[0] = [[G.nodes[node]['x'],G.nodes[node]['y']] for node in self.optimal_path[0]]
        return shortest_route_metadata, self.optimal_path
