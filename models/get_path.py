# from typing_extensions import Required
from map_utility import Map
from algorithms_utility import Algorthms

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

        

        return None


