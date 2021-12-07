from flask import request
from flask_restful import Resource, reqparse
from numpy.lib.utils import source
from osmnx.elevation import add_node_elevations
from pandas.core.indexes import api

from models.algorithms import Algorithms

import requests
import time
import json
import math
import os

import networkx as nx
import pandas as pd
import osmnx as ox
import pickle as p


class MainModel(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("source_coords_lat",
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument("source_coords_long",
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument("destination_coords_lat",
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument("destinations_coords_long",
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument("is_elevation_max",
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument("percentage",
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument("algorithm",
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )


    def post(self):
        data = self.parser.parse_args()

        source_coords_lat = float(data["source_coords_lat"])
        source_coords_long = float(data["source_coords_long"])
        source_coords = (source_coords_lat, source_coords_long)

        destination_coords_lat = float(data["destination_coords_lat"])
        destinations_coords_long = float(data["destinations_coords_long"])
        destination_coords = (destination_coords_lat, destinations_coords_long)

        is_max = data["is_elevation_max"]
        percentage = int(data["percentage"])
        algo = data["algorithm"]

        if os.path.exists("./graph.p"):
            map = p.load( open( "graph.p", "rb" ) )
            print("Loaded Graph")
        else:
            map = self.generate_map(source_coords)

        algo = Algorithms(map, percentage, is_max)
        shortestPath, elevPath = algo.shortest_path(source_coords, destination_coords, percentage, algo, is_max)

        if shortestPath is None and elevPath is None:
            data = {"elevation_route" : [] , "shortest_route" : []}        
            data["shortDist"] = 0
            data["gainShort"] = 0
            data["dropShort"] = 0
            data["elenavDist"]  = 0
            data["gainElenav"] = 0
            data["dropElenav"] = 0
            data["popup_flag"] = 0 
            return data
        data = {"elevation_route" : self.make_geojson(elevPath[0]), "shortest_route" : self.make_geojson(shortestPath[0])}
        data["shortDist"] = shortestPath[1]
        data["gainShort"] = shortestPath[2]
        data["dropShort"] = shortestPath[3]  
        data["elenavDist"] = elevPath[1]
        data["gainElenav"] = elevPath[2]
        data["dropElenav"] = elevPath[3] 
        if len(elevPath[0])==0:
            data["popup_flag"] = 1        
        else:
            data["popup_flag"] = 2    
        return data


    def generate_map(self, source):
        map = ox.graph_from_point(source, dist=20000, network_type="walk")
        map = self.add_elevation_to_node(map)

        p.dump(map, open( "graph.p", "wb" ) )
        print("Saved Graph")

        return map


    def add_elevation_to_node(self, graph, max_locations_per_batch=150, pause_duration=0.02, precision=3):

        url_template = 'https://api.open-elevation.com/api/v1/lookup?locations={}'
        node_points = pd.Series({node: '{:.5f},{:.5f}'.format(data['y'], data['x']) for node, data in graph.nodes(data=True)})

        number_api_calls = math.ceil(len(node_points) / max_locations_per_batch)

        results = []
        for i in range(0, len(node_points), max_locations_per_batch):
            chunk = node_points.iloc[i: i + max_locations_per_batch]
            locations = '|'.join(chunk)
            url = url_template.format(locations)
            try:
                time.sleep(pause_duration)
                response = requests.get(url)
                response_json = response.json()
            except Exception as e:
                print(e)

            results.extend(response_json['results'])

        if not (len(results) == len(graph.nodes()) == len(node_points)):
            raise Exception('Graph has {} nodes but we received {} results from the elevation API.'.format(len(graph.nodes()),
                                                                                                           len(results)))
        else:
            pass

        df = pd.DataFrame(node_points, columns=['node_points'])
        df['elevation'] = [result['elevation'] for result in results]
        df['elevation'] = df['elevation'].round(precision)  
        nx.set_node_attributes(graph, name='elevation', values=df['elevation'].to_dict())

        return graph

    def make_geojson(self, coordinates):
        geojson = {}
        geojson["properties"] = {}
        geojson["type"] = "Feature"
        geojson["geometry"] = {}
        geojson["geometry"]["type"] = "LineString"
        geojson["geometry"]["coordinates"] = coordinates

        return geojson
