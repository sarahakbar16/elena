import osmnx as ox
import networkx as nx

from heapq import *
import matplotlib.pyplot as plt
from collections import deque, defaultdict

class ElevationAlgorithms:

    def __init__(self, G, percentage = 0.0, is_max = True):
        self.G = G
        self.is_max = is_max
        self.percentage = percentage
        self.optimal_path = [[], 0.0, float('-inf'), 0.0]
        self.source_node, self.destination_node = None, None


    def verify_valid_nodes(self):
        if self.source_node is None or self.destination_node is None:
            return False
        return True

    def astar(self):
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

        f_score[source_node] = G.nodes[source_node]['dist_from_dest']

        while len(open_set):
            current_node = min([(node,f_score[node]) for node in open_set], key=lambda t: t[1])[0]
            if current_node == destination_node:
                  if not last_node or not current_node : return
                  total_path = [current_node]
                  while current_node in lastNode:
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

                approx_g_score = g_score[current_node] + self.elevation_difference(current_node, neighbor, "gain")
                approx_g_score1 = g_score1[current_node] + self.elevation_difference(current_node, neighbor, "normal")
                if neighbor not in open_set and tentative_g_score1<=(1+percentage)*shortest_distance:
                    openSet.add(nei)
                else:
                    if approx_g_score >= g_score[neighbor] or approx_g_score1>=(1+percentage)*shortest_distance:
                        continue 
                last_node[neighbor] = current_node
                g_score[neighbor] = approx_g_score
                g_score1[neighbor] = approx_g_score1
                f_score[neighbor] = g_score[neighbor] + G.nodes[neighbor]['dist_from_dest']


    def elevation_difference(self, node1, node2, min_max = "normal"):
        G = self.G

        if node1 is None or node2 is None : return
        
        if min_max == "normal":
            try : return G.edges[node1, node2 ,0]["length"]
            except : return G.edges[node1, node2]["weight"]
        
        elif min_max == "gain":
            return max(0.0, G.nodes[node2]["elevation"] - G.nodes[node1]["elevation"])

        elif min_max == "final-elevation":
            return G.nodes[node2]["elevation"] - G.nodes[node1]["elevation"]
        
        elif min_max == "drop":
            return max(0.0, G.nodes[node1]["elevation"] - G.nodes[node2]["elevation"])
        
        else:
            return abs(G.nodes[node1]["elevation"] - G.nodes[node2]["elevation"])

    
    def compute_elevation(self, path, min_max = "final-elevation", piece_wise = False):
        
        total_elevation = 0
        
        if piece_wise : piece_wise_elevations = []
        
        for i in range(len(path)-1):

            if min_max == "final-elevation":
                elevation_difference = self.elevation_difference(path[i], path[i+1], "final-elevation")
            
            elif min_max == "gain":
                elevation_difference = self.elevation_difference(path[i],path[i+1],"gain")
            
            elif min_max == "drop":
                elevation_difference = self.elevation_difference(path[i],path[i+1],"drop")
            
            elif min_max == "normal":
                elevation_difference = self.elevation_difference(path[i],path[i+1],"normal")
            
            total_elevation = total_elevation + elevation_difference
            
            if piece_wise : piece_wise_elevations.append(elevation_difference)
        
        if piece_wise:
            return total_elevation, piece_wise_elevations
        
        else:
            return total_elevation


    def get_path(self, parent, destination):

        route = [destination]
        
        current = parent[destination]
        
        while current != -1:
            route.append(current)
            current = parent[current]
        
        return route[::-1]


    def dijkstra(self, edge_value):

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
                    elevation_diff = self.elevation_difference(current_node, neighbors, "normal")

                    if is_max :
                        if edge_value[0] == 1:
                            next_elevation_diff = elevation_diff - self.elevation_difference(current_node, neighbors, "final-elevation")
                        elif edge_value[0] == 2:
                            next_elevation_diff = (elevation_diff - self.elevation_difference(current_node, neighbors, "final-elevation"))*elevation_diff
                        elif edge_value[0] == 3:
                            next_elevation_diff = elevation_diff + self.elevation_difference(current_node, neighbors, "drop")
                    else:
                        if edge_value[0] == 1:
                            next_elevation_diff = elevation_diff + self.elevation_difference(current_node, neighbors, "final-elevation")
                        elif edge_value[0] == 2:
                            next_elevation_diff = (elevation_diff + self.elevation_difference(current_node, neighbors, "final-elevation"))*elevation_diff
                        else:
                            next_elevation_diff = elevation_diff + self.elevation_difference(current_node, neighbors, "gain")
                    
                    if edge_value[1]:
                         next_elevation_diff = next_elevation_diff + current_priority
                    
                    next_distance = current_distance + elevation_diff
                    if next_distance <= shortest_distance*(1.0+percentage) and (previous is None or next_elevation_diff < previous):
                        parent_dict[neighbors] = current_node
                        minimum_distances[neighbors] = next_elevation_diff
                        heappush(queue, (next_elevation_diff, next_distance, neighbors))

        return None, None, None


    def djikstra_all_paths(self):
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


    def calculate_shortest_path(self, start_location, end_location, percentage, algorithm, is_max):
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
            self.astar()
        else :
            print("Dijkstra algorithm is being used to calculate path with elevation.")
            self.djikstra_all_paths()

        shortest_route_coordinates = [[G.nodes[node]['x'],G.nodes[node]['y']] for node in self.shortest_route]
        shortest_route_metadata = [shortest_route_coordinates, self.shortest_distance, \
                            self.compute_elevation(self.shortest_route, "gain"), self.compute_elevation(self.shortest_route, "drop")]

        if (self.is_max  and self.optimal_path[2] == float('-inf')) or (not self.is_max and self.optimal_path[3] == float('-inf')):
            return shortest_route_metadata, [[], 0.0, 0, 0]

        self.optimal_path[0] = [[G.nodes[node]['x'],G.nodes[node]['y']] for node in self.optimal_path[0]]
        return shortest_route_metadata, self.optimal_path
