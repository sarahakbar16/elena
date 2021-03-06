# from typing_extensions import Required
from models.map_utility import Map
from models.algorithms_utility import ElevationAlgorithms

from flask import request
from flask_restful import Resource, reqparse

import osmnx

import networkx as nx


class GetPath(Resource):

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
        algorithm = data["algorithm"]

        if is_max == "True":
            is_max = True
        else:
            is_max = False

        
        # create map
        map_obj = Map()
        map = map_obj.generate_map(source_coords)

        # call method to find shortest_path
        algo = ElevationAlgorithms(map, percentage, is_max)
        shortest_path, elevation_path = algo.calculate_shortest_path(source_coords, destination_coords, percentage, algorithm, is_max)

        if shortest_path is None and elevation_path is None:
            geojson = {"elevation_path": [], "shortest_path": []}
            geojson["shortest_dist"] = 0
            geojson["shortest_gain"] = 0
            geojson["elevation_dist"] = 0
            geojson["elevation_gain"] = 0
            geojson["popup_flag"] = 0
            return geojson

        # send output to UI
        geojson_chunk_ele = {}
        geojson_chunk_ele["properties"] = {}
        geojson_chunk_ele["type"] = "Feature"
        geojson_chunk_ele["geometry"] = {}
        geojson_chunk_ele["geometry"]["type"] = "LineString"
        geojson_chunk_ele["geometry"]["coordinates"] = elevation_path[0]

        geojson = {}
        geojson["elevation_path"] = geojson_chunk_ele


        geojson_chunk_s = {}
        geojson_chunk_s["properties"] = {}
        geojson_chunk_s["type"] = "Feature"
        geojson_chunk_s["geometry"] = {}
        geojson_chunk_s["geometry"]["type"] = "LineString"
        geojson_chunk_s["geometry"]["coordinates"] = shortest_path[0]

        geojson["shortest_path"] = geojson_chunk_s
        geojson["shortest_dist"] = shortest_path[1]
        geojson["shortest_gain"] = shortest_path[2]
        geojson["elevation_dist"] = elevation_path[1]
        geojson["elevation_gain"] = elevation_path[2]

        if len(elevation_path[0])==0:
            geojson["popup_flag"] = 1        
        else:
            geojson["popup_flag"] = 2    
        return geojson
