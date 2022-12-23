from src.aoc2022 import utils
from src.aoc2022.days import day16


class TestDay15:
    def test_parse_data_to_graph(self):
        # Prepare
        test_data_path = "./unittests/2022/test_data/day16_sample.txt"
        input_data = utils.get_raw_data(test_data_path)

        expected_flow_rates = {
            "AA": 0,
            "BB": 13,
            "CC": 2,
            "DD": 20,
            "EE": 3,
            "FF": 0,
            "GG": 0,
            "HH": 22,
            "II": 0,
            "JJ": 21,
        }

        expected_connections = {
            "AA": ["DD", "II", "BB"],
            "BB": ["CC", "AA"],
            "CC": ["DD", "BB"],
            "DD": ["CC", "AA", "EE"],
            "EE": ["FF", "DD"],
            "FF": ["EE", "GG"],
            "GG": ["FF", "HH"],
            "HH": ["GG"],
            "II": ["AA", "JJ"],
            "JJ": ["II"],
        }

        expected_valves = sorted(list(expected_flow_rates.keys()))

        # Run
        actual_graph = day16.parse_data_to_graph(input_data)

        # Assert
        assert actual_graph.connections == expected_connections
        assert actual_graph.get_flow_rates() == expected_flow_rates
        assert sorted(actual_graph.get_valves()) == sorted(expected_valves)

    def test_get_optimal_sequence(self):
        # Prepare
        test_data_path = "./unittests/2022/test_data/day16_sample.txt"
        input_data = utils.get_raw_data(test_data_path)
        graph = day16.parse_data_to_graph(input_data)

        expected_sequence = [
            ("AA", 30),
            ("DD", 28),
            ("BB", 25),
            ("JJ", 21),
            ("HH", 13),
            ("EE", 9),
            ("CC", 6),
        ]
        expected_score = 1651

        start_node = "AA"
        total_time = 30

        # Run
        actual_sequence, actual_score = day16.get_optimal_sequence(
            graph, start_node, total_time
        )

        # Assert
        assert actual_sequence == expected_sequence
        assert actual_score == expected_score

    def test_get_optimal_dual_sequence(self):
        # Prepare
        test_data_path = "./unittests/2022/test_data/day16_sample.txt"
        input_data = utils.get_raw_data(test_data_path)
        graph = day16.parse_data_to_graph(input_data)

        expected_sequence_1 = [("AA", 26), ("JJ", 23), ("BB", 19), ("CC", 17)]
        expected_sequence_2 = [("AA", 26), ("DD", 24), ("HH", 19), ("EE", 15)]
        expected_score = 1707

        start_node = "AA"
        total_time = 26

        # Run
        actual_p1, actual_p2, actual_score = day16.get_optimal_dual_sequence(
            graph, start_node, total_time
        )

        # Assert
        assert actual_p1 == expected_sequence_1
        assert actual_p2 == expected_sequence_2
        assert actual_score == expected_score
