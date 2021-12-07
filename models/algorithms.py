import osmnx as ox
import networkx as nx

from heapq import *
import matplotlib.pyplot as plt
from collections import deque, defaultdict

class Algorithms:

    def __init__(self, G, percentage = 0.0, maxMin = "maximize"):
        self.G = G
        self.maxMin = maxMin
        self.percentage = percentage
        self.optimalPath = [[], 0.0, float('-inf'), 0.0]
        self.sourceNode, self.destinationNode = None, None


    def verify_valid_nodes(self):
        if self.sourceNode is None or self.destinationNode is None:
            return False
        return True


    def reconstruct_path(self, lastNode, currentNode):
        if not lastNode or not currentNode : return
        total_path = [currentNode]
        while currentNode in lastNode:
            currentNode = lastNode[currentNode]
            total_path.append(currentNode)
        self.optimalPath = [total_path[:], self.compute_elevation(total_path, "normal"), self.compute_elevation(total_path, "gain-only"), \
                                                                        self.compute_elevation(total_path, "drop-only")]
        return


    def astar(self):
        if not self.verify_valid_nodes() : return
        G, shortest = self.G, self.shortest_dist
        percentage, maxMin = self.percentage, self.maxMin
        sourceNode, destinationNode = self.sourceNode, self.destinationNode

        closedSet = set()

        openSet = set()
        openSet.add(sourceNode)

        cameFrom = {}

        gScore = {}
        for node in G.nodes():
            gScore[node] = float("inf")

        gScore[sourceNode] = 0

        gScore1 = {}
        for node in G.nodes():
            gScore1[node] = float("inf")

        gScore1[sourceNode] = 0

        fScore = {}

        fScore[sourceNode] = G.nodes[sourceNode]['dist_from_dest']

        while len(openSet):
            current = min([(node,fScore[node]) for node in openSet], key=lambda t: t[1])[0]
            if current == destinationNode:
                self.reconstruct_path(cameFrom, current)
                return

            openSet.remove(current)
            closedSet.add(current)
            for nei in G.neighbors(current):
                if nei in closedSet:
                    continue 

                tentative_gScore = gScore[current] + self.get_cost(current, nei, "gain-only")
                tentative_gScore1 = gScore1[current] + self.get_cost(current, nei, "normal")
                if nei not in openSet and tentative_gScore1<=(1+percentage)*shortest:
                    openSet.add(nei)
                else:
                    if tentative_gScore >= gScore[nei] or tentative_gScore1>=(1+percentage)*shortest:
                        continue 
                cameFrom[nei] = current
                gScore[nei] = tentative_gScore
                gScore1[nei] = tentative_gScore1
                fScore[nei] = gScore[nei] + G.nodes[nei]['dist_from_dest']


    def get_cost(self, n1, n2, maxMin = "normal"):
        G = self.G
        if n1 is None or n2 is None : return
        if maxMin == "normal":
            try : return G.edges[n1, n2 ,0]["length"]
            except : return G.edges[n1, n2]["weight"]
        elif maxMin == "elevation-diff":
            return G.nodes[n2]["elevation"] - G.nodes[n1]["elevation"]
        elif maxMin == "gain-only":
            return max(0.0, G.nodes[n2]["elevation"] - G.nodes[n1]["elevation"])
        elif maxMin == "drop-only":
            return max(0.0, G.nodes[n1]["elevation"] - G.nodes[n2]["elevation"])
        else:
            return abs(G.nodes[n1]["elevation"] - G.nodes[n2]["elevation"])


    def depth_first_search(self, sourceNode, destinationNode, currDist = 0.0, elevGain = 0.0, elevDrop = 0.0, path = [], visited = set()):
        if not self.verify_valid_nodes() : return

        if currDist > self.shortest_dist*(1.0+self.percentage):
            return

        if sourceNode == destinationNode:
            if self.maxMin == "maximize" and self.optimalPath[2] < elevGain:
                self.optimalPath = [path[:], currDist, elevGain, elevDrop]
            elif self.maxMin == "minimize" and self.optimalPath[2] > elevGain :
                self.optimalPath = [path[:], currDist, elevGain, elevDrop]
            return

        visited.add(sourceNode)

        for nei in self.G.neighbors(sourceNode):
            if nei not in visited:
                distCost = currDist + self.get_cost(sourceNode, nei)
                gainCost = elevGain + self.get_cost(sourceNode, nei, "gain-only")
                dropCost = elevDrop + self.get_cost(sourceNode, nei, "drop-only")
                self.depth_first_search(nei, destinationNode, distCost, gainCost, dropCost, path + [nei])

        visited.remove(sourceNode)
        return


    def compute_elevation(self, route, maxMin = "both", piecewise = False):
        total = 0
        if piecewise : piecewiseElevs = []
        for i in range(len(route)-1):
            if maxMin == "both":
                diff = self.get_cost(route[i],route[i+1],"elevation-diff")
            elif maxMin == "gain-only":
                diff = self.get_cost(route[i],route[i+1],"gain-only")
            elif maxMin == "drop-only":
                diff = self.get_cost(route[i],route[i+1],"drop-only")
            elif maxMin == "normal":
                diff = self.get_cost(route[i],route[i+1],"normal")
            total += diff
            if piecewise : piecewiseElevs.append(diff)
        if piecewise:
            return total, piecewiseElevs
        else:
            return total


    def get_route(self, parent, dest):
        path = [dest]
        curr = parent[dest]
        while curr!=-1:
            path.append(curr)
            curr = parent[curr]
        return path[::-1]


    def dijkstra(self, weight):
        if not self.verify_valid_nodes() : return
        G, percentage, shortest, maxMin = self.G, self.percentage, self.shortest_dist, self.maxMin
        sourceNode, destinationNode = self.sourceNode, self.destinationNode
        q, seen, mins = [(0.0, 0.0, sourceNode)], set(), {sourceNode: 0}

        parent = defaultdict(int)
        parent[sourceNode] = -1
        while q:
            currPriority, currDist, node = heappop(q)

            if node not in seen:
                seen.add(node)
                if node == destinationNode:
                    return currPriority, currDist, parent

                for nei in G.neighbors(node):
                    if nei in seen: continue
                    prev = mins.get(nei, None)
                    length = self.get_cost(node, nei, "normal")

                    if maxMin == "maximize":
                        if weight[0] == 1:
                            next = length - self.get_cost(node, nei, "elevation-diff")
                        elif weight[0] == 2:
                            next = (length - self.get_cost(node, nei, "elevation-diff"))*length
                        elif weight[0] == 3:
                            next = length + self.get_cost(node, nei, "drop-only")
                    else:
                        if weight[0] == 1:
                            next = length + self.get_cost(node, nei, "elevation-diff")
                        elif weight[0] == 2:
                            next = (length + self.get_cost(node, nei, "elevation-diff"))*length
                        else:
                            next = length + self.get_cost(node, nei, "gain-only")
                    if weight[1] : next += currPriority
                    nextDist = currDist + length
                    if nextDist <= shortest*(1.0+percentage) and (prev is None or next < prev):
                        parent[nei] = node
                        mins[nei] = next
                        heappush(q, (next, nextDist, nei))

        return None, None, None


    def djikstra_all_paths(self):
        if not self.verify_valid_nodes() : return
        sourceNode, destinationNode = self.sourceNode, self.destinationNode


        for weight in [[1, True], [2, True], [3, True], [1, False], [2, False], [3, False]]:
            _, currDist, parent = self.dijkstra(weight)

            if not currDist : continue

            route = self.get_route(parent, destinationNode)
            elevDist, dropDist = self.compute_elevation(route, "gain-only"), self.compute_elevation(route, "drop-only")
            if self.maxMin == "maximize":
                if (elevDist > self.optimalPath[2]) or (elevDist == self.optimalPath[2] and currDist < self.optimalPath[1]):
                    self.optimalPath = [route[:], currDist, elevDist, dropDist]
            else:
                if (elevDist < self.optimalPath[2]) or (elevDist == self.optimalPath[2] and currDist < self.optimalPath[1]):
                    self.optimalPath = [route[:], currDist,  elevDist, dropDist]

        return


    def shortest_path(self, start_location, end_location, percentage, algo = "djikstra", maxMin = "maximize", log = True):
        G = self.G
        self.percentage = percentage/100.0
        self.maxMin = maxMin
        self.sourceNode, self.destinationNode = None, None

        if maxMin == "maximize" : self.optimalPath = [[], 0.0, float('-inf'), float('-inf')]
        else : self.optimalPath = [[], 0.0, float('inf'), float('-inf')]

        self.sourceNode, d1 = ox.get_nearest_node(G, point=start_location, return_dist = True)
        self.destinationNode, d2   = ox.get_nearest_node(G, point=end_location, return_dist = True)
        if d1 > 1000 or d2 > 1000:
            if log : print("Nodes too far")
            return None, None

        self.shortest_route = nx.shortest_path(G, source=self.sourceNode, target=self.destinationNode, weight='length')
        self.shortest_dist  = sum(ox.utils_graph.get_route_edge_attributes(G, self.shortest_route, 'length'))


        if algo == "astar" or maxMin=="minimize":
            if log : print("astar")
            self.astar()

        if log : print("dijkstra")
        self.djikstra_all_paths()
        shortest_route_latlong = [[G.nodes[route_node]['x'],G.nodes[route_node]['y']] for route_node in self.shortest_route]
        shortestPathStats = [shortest_route_latlong, self.shortest_dist, \
                            self.compute_elevation(self.shortest_route, "gain-only"), self.compute_elevation(self.shortest_route, "drop-only")]

        if (self.maxMin == "maximize" and self.optimalPath[2] == float('-inf')) or (self.maxMin == "minimize" and self.optimalPath[3] == float('-inf')):
            return shortestPathStats, [[], 0.0, 0, 0]

        self.optimalPath[0] = [[G.nodes[route_node]['x'],G.nodes[route_node]['y']] for route_node in self.optimalPath[0]]
        return shortestPathStats, self.optimalPath
