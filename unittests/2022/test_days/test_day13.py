import random

import pytest

from src.aoc2022 import utils
from src.aoc2022.days import day13


class TestDay13:
    def test_parse_data_to_array(self):
        # Prepare
        test_data_path = "./unittests/2022/test_data/day13_sample.txt"
        input_data = utils.get_raw_data(test_data_path)

        expected_packets = [
            ([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]),
            ([[1], [2, 3, 4]], [[1], 4]),
            ([9], [[8, 7, 6]]),
            ([[4, 4], 4, 4], [[4, 4], 4, 4, 4]),
            ([7, 7, 7, 7], [7, 7, 7]),
            ([], [3]),
            ([[[]]], [[]]),
        ]

        # Run
        actual_packets = day13.parse_data_to_array(input_data)

        # Assert
        assert actual_packets == expected_packets

    @pytest.mark.parametrize(
        "l_packet, r_packet, expected_equality",
        [
            ([1, 1, 3, 1, 1], [1, 1, 5, 1, 1], 1),
            ([[1], [2, 3, 4]], [[1], 4], 1),
            ([9], [[8, 7, 6]], -1),
            ([[4, 4], 4, 4], [[4, 4], 4, 4, 4], 1),
            ([7, 7, 7, 7], [7, 7, 7], -1),
            ([], [3], 1),
            ([[[]]], [[]], -1),
            (
                [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
                [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
                -1,
            ),
        ],
    )
    def test_element_is_equal(self, l_packet, r_packet, expected_equality):
        # Prepare

        # Run
        actual_equality = day13.element_is_equal(l_packet, r_packet)

        # Assert
        assert expected_equality == actual_equality

    def test_sort_packets(self):
        # Prepare
        expected_packets = [
            [],
            [[]],
            [[[]]],
            [1, 1, 3, 1, 1],
            [1, 1, 5, 1, 1],
            [[1], [2, 3, 4]],
            [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
            [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
            [[1], 4],
            [[2]],
            [3],
            [[4, 4], 4, 4],
            [[4, 4], 4, 4, 4],
            [[6]],
            [7, 7, 7],
            [7, 7, 7, 7],
            [[8, 7, 6]],
            [9],
        ]

        random.seed(1234)
        shuffled_packets = [e for e in expected_packets]
        random.shuffle(shuffled_packets)

        # Run
        sorted_packets = day13.sort_packets(shuffled_packets)

        # Assert
        assert expected_packets == sorted_packets
