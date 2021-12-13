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

        if algorithm == "True":
            algorithm = True
        else:
            algorithm = False

        
        # create map
        map_obj = Map()
        map = map_obj.generate_map(source_coords)

        # call method to find shortest_path
        algorithm = ElevationAlgorithms(map, percentage, is_max)
        shortest_path, elevation_path = algorithm.calculate_shortest_path(source_coords, destination_coords, percentage, algorithm, is_max)


        # send output to UI
        geojson_chunk = {}
        geojson_chunk["properties"] = {}
        geojson_chunk["type"] = "Feature"
        geojson_chunk["geometry"] = {}
        geojson_chunk["geometry"]["type"] = "LineString"
        geojson_chunk["geometry"]["coordinates"] = elevation_path[0]

        geojson = {}
        geojson["elevation_path"] = geojson_chunk

        geojson_chunk["geometry"]["coordinates"] = shortest_path[0]

        geojson["shortest_path"] = geojson_chunk
        geojson["shortest_dist"] = shortest_path[1]  # in m 
        geojson["shortest_gain"] = shortest_path[2]
        # data["dropShort"] = shortestPath[3]  
        geojson["elevation_dist"] = elevation_path[1]
        geojson["elevation_gain"] = elevation_path[2]
        # data["dropElenav"] = elevPath[3] 
        if len(elevation_path[0])==0:
            geojson["popup_flag"] = 1        
        else:
            geojson["popup_flag"] = 2    
        return geojson

