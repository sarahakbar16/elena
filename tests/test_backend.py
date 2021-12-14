import unittest

from models.map_utility import Map
from models.algorithms_utility import ElevationAlgorithms


class Test(unittest.TestCase):

    def setUp(self):
        self.map = Map().generate_map((42.406538, -72.530997))
        self.algorithm_obj = ElevationAlgorithms(self.map, percentage=100, is_max=True)

    def tearDown(self):
        pass

    def test_is_not_valid_location(self):
        """
        Testing if the verify_valid_nodes() method returns None for invalid nodes
        """
        self.algorithm_obj = ElevationAlgorithms(self.map, percentage=100, is_max=True)
        self.algorithm_obj.source_node = None
        self.algorithm_obj.destination_node = None

        self.assertFalse(self.algorithm_obj.verify_valid_nodes())

    def test_valid_location(self):
        """
        Testing if the verify_valid_nodes() method returns not None for valid nodes
        """
        shortest_path, elevation_path = self.algorithm_obj.calculate_shortest_path(
            (42.406538, -72.530997),
            (42.346851,  -72.52751),
            percentage=100,
            algorithm="dijkstra",
            is_max=True)

        self.assertTrue(self.algorithm_obj.verify_valid_nodes())
        self.assertIsNotNone(shortest_path)
        self.assertIsNotNone(elevation_path)

    def test_calc_elevation_dist(self):
        shortest_path, elevation_path = self.algorithm_obj.calculate_shortest_path(
            (42.406538, -72.530997),
            (42.346851, -72.52751),
            percentage=150,
            algorithm="dijkstra",
            is_max=True)
        percentage = 150

        # shortest_dist
        self.assertGreater(shortest_path[1] + (shortest_path[1] * percentage/100), elevation_path[1])

    def test_calc_route_elevation(self):
        shortest_path, elevation_path = self.algorithm_obj.calculate_shortest_path(
            (42.406538, -72.530997),
            (42.346851, -72.52751),
            percentage=100,
            algorithm="dijkstra",
            is_max=True)

        self.assertEqual(elevation_path[2], 275.0)

    def test_dijkstra(self):
        _, elevation_path = self.algorithm_obj.calculate_shortest_path(
            (42.406538, -72.530997),
            (42.346851, -72.52751),
            percentage=150,
            algorithm="dijkstra",
            is_max=False)

        self.assertEqual(elevation_path[1], 7206.064999999997)
        self.assertEqual(elevation_path[2], 75.0)

    def test_astar(self):
        _, elevation_path = self.algorithm_obj.calculate_shortest_path(
            (42.406538, -72.530997),
            (42.346851, -72.52751),
            percentage=150,
            algorithm="astar",
            is_max=False)

        self.assertEqual(elevation_path[1], 11880.708999999999)
        self.assertEqual(elevation_path[2], 103.0)
