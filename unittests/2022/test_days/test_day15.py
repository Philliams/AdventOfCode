import pytest

from src.aoc2022 import utils
from src.aoc2022.days import day15


class TestDay15:
    def test_parse_data_to_array(self):
        # Prepare
        test_data_path = "./unittests/2022/test_data/day15_sample.txt"
        input_data = utils.get_raw_data(test_data_path)

        expected_parsed_data = [
            (2, 18, -2, 15),
            (9, 16, 10, 16),
            (13, 2, 15, 3),
            (12, 14, 10, 16),
            (10, 20, 10, 16),
            (14, 17, 10, 16),
            (8, 7, 2, 10),
            (2, 0, 2, 10),
            (0, 11, 2, 10),
            (20, 14, 25, 17),
            (17, 20, 21, 22),
            (16, 7, 15, 3),
            (14, 3, 15, 3),
            (20, 1, 15, 3),
        ]

        # Run
        actual_parsed_data = day15.parse_data_to_array(input_data)

        # Assert
        assert actual_parsed_data == expected_parsed_data

    @pytest.mark.parametrize(
        "line_number, expected_count",
        [
            (9, 25),
            (10, 26),
            (11, 28),
        ],
    )
    def test_count_scanned_location(self, line_number, expected_count):
        # Prepare
        test_data_path = "./unittests/2022/test_data/day15_sample.txt"
        input_data = utils.get_raw_data(test_data_path)
        parsed_data = day15.parse_data_to_array(input_data)

        # Run
        actual_result = day15.count_scanned_location(parsed_data, line_number)
        _, actual_count = actual_result

        # Assert
        assert actual_count == expected_count

    @pytest.mark.parametrize(
        "line_number, expected_count, expected_ranges",
        [
            (9, 21, [(0, 20)]),
            (10, 20, [(0, 20)]),
        ],
    )
    def test_count_scanned_location_with_bounds(
        self, line_number, expected_count, expected_ranges
    ):
        # Prepare
        test_data_path = "./unittests/2022/test_data/day15_sample.txt"
        input_data = utils.get_raw_data(test_data_path)
        parsed_data = day15.parse_data_to_array(input_data)

        bounding_range = (0, 20)

        # Run
        actual_ranges, actual_count = day15.count_scanned_location(
            parsed_data, line_number, bounding_range
        )

        # Assert
        assert actual_count == expected_count
        assert actual_ranges == expected_ranges

    def test_count_scanned_location_with_overlapping(self):
        # Prepare
        input_ranges = [(0, 0, 0, 1), (5, 0, 5, 1)]

        line_number = 0

        expected_ranges = [(-1, 1), (4, 6)]
        expected_count = 6

        # Run
        actual_ranges, actual_count = day15.count_scanned_location(
            input_ranges, line_number
        )

        # Assert
        assert expected_ranges == actual_ranges
        assert actual_count == expected_count
