import os
import time
import requests


import pickle as p
import osmnx as ox
import pandas as pd
import networkx as nx

class Map:
    
    def __init__(self):
        self.open_elevation_url = 'https://api.open-elevation.com/api/v1/lookup?locations={}'

    def generate_map(self, source):
        if os.path.exists("./amherst.map"):
            print("Loading Map..")
            map = p.load(open("amherst.map", "rb"))
        else:
            map = ox.graph_from_point(source, dist=20000, network_type="walk")
            map = self.add_elevation_to_node(map)

            p.dump(map, open( "amherst.map", "wb" ))
            print("Graph Saved")

        return map

    def add_elevation_to_node(self, map, max_locations_per_batch=150, pause_time=0.02, precision=3):
        points_node = pd.Series({
            node: '{:.5f},{:.5f}'.format(data['y'], data['x']) 
            for node, data in map.nodes(data=True)
            })

        results = []
        for i in range(0, len(points_node), max_locations_per_batch):
            locations = '|'.join(points_node.iloc[i: i + max_locations_per_batch])
            url = self.open_elevation_url.format(locations)
            try:
                time.sleep(pause_time)
                response = requests.get(url)
                response_json = response.json()
            except Exception as e:
                print(e)

            results.extend(response_json['results'])

        if not (len(results) == len(map.nodes()) == len(points_node)):
            raise Exception('Graph has {} nodes but we received {} results from the elevation API.'.format(len(map.nodes()),
                                                                                                           len(results)))

        df = pd.DataFrame(points_node, columns=['node_points'])  # check
        df['elevation'] = [result['elevation'] for result in results]
        df['elevation'] = df['elevation'].round(precision)  
        nx.set_node_attributes(map, name='elevation', values=df['elevation'].to_dict())

        return map
