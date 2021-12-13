# from typing_extensions import Required
from flask import request
from flask_restful import Resource, reqparse

import osmnx

import networkx as nx


class GetPath(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('source',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('destination',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('is_elevation_max',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('percentage',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('algorithm',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )


    def post(self):
        data = self.parser.parse_args()
        
        source = "umass police station"
        destintion = "puffton village apartments"

        source_coord = osmnx.geocoder.geocode(source)
        destination_coord = osmnx.geocoder.geocode(destintion)
        is_max = True
        percentage = 50
        print(source_coord)
        print(destination_coord)

        params = dict()
        params['city']  = "Amherst"
        params['state'] = "Massachusetts"
        params['country'] = 'USA'
        graph = osmnx.graph_from_place(params, network_type='drive')

        # call methods to 
        # gen map
        # find node ids
        # add elevation
        # call algo

        return None


