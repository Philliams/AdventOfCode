import numpy as np

from src.aoc2022 import utils
from src.aoc2022.days import day12


class TestDay12:
    def test_parse_data_to_array(self):
        # Prepare
        test_data_path = "./unittests/2022/test_data/day12_sample.txt"
        input_data = utils.get_raw_data(test_data_path)

        expected_start = (0, 0)
        expected_end = (5, 2)
        expected_data = np.array(
            [
                [0, 0, 1, 16, 15, 14, 13, 12],
                [0, 1, 2, 17, 24, 23, 23, 11],
                [0, 2, 2, 18, 25, 25, 23, 10],
                [0, 2, 2, 19, 20, 21, 22, 9],
                [0, 1, 3, 4, 5, 6, 7, 8],
            ]
        ).transpose()

        # Run
        actual_result = day12.parse_data_to_array(input_data)
        actual_data, actual_start, actual_end = actual_result

        # Assert
        assert actual_start == expected_start
        assert actual_end == expected_end
        assert (actual_data == expected_data).all()

    def test_find_path_length(self):
        # Prepare
        test_data_path = "./unittests/2022/test_data/day12_sample.txt"
        input_data = utils.get_raw_data(test_data_path)
        parsed_map, start, end = day12.parse_data_to_array(input_data)

        expected_distance = 31

        # Run
        distance_matrix = day12.get_distance_matrix(parsed_map, end)
        actual_distance = distance_matrix[start]

        # Assert

        assert actual_distance == expected_distance

    def test_find_closest_start_point(self):
        # Prepare
        test_data_path = "./unittests/2022/test_data/day12_sample.txt"
        input_data = utils.get_raw_data(test_data_path)
        parsed_map, start, end = day12.parse_data_to_array(input_data)

        expected_clostest_start = 29

        # Run
        distance_matrix = day12.get_distance_matrix(parsed_map, end)
        actual_clostest_start = distance_matrix[parsed_map == 0].min()

        # Assert

        assert expected_clostest_start == actual_clostest_start
