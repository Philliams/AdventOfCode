import numpy as np
import pytest

from src.aoc2022.days import day8

sample_data = """30373
25512
65332
33549
35390"""

parsed_data = np.array(
    [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]
)


class TestDay8:
    def test_parse_data(self):
        # Prepare
        raw_input = sample_data
        expected_result = parsed_data.copy()
        # Run
        actual_result = day8.parse_data_to_array(raw_input)

        # Assert
        assert (expected_result == actual_result).all()

    @pytest.mark.parametrize(
        "values, expected_visible",
        [
            ([3, 0, 3, 7, 3], 3),
            ([2, 5, 5, 1, 2], 4),
            ([6, 5, 3, 3, 2], 4),
            ([3, 3, 5, 4, 9], 3),
            ([3, 5, 3, 9, 0], 4),
        ],
    )
    def test_scan_height_row(self, values, expected_visible):
        # Prepare
        vals = np.array(values)

        # Run
        actual_visible = day8.scan_height_row(vals)

        # Assert
        assert len(actual_visible) == expected_visible

    def test_count_visible_trees(self):
        # Prepare
        height_map = parsed_data.copy()
        expected_visible = 21

        # Run
        actual_visible = day8.count_visible_trees(height_map)

        # Assert
        assert expected_visible == actual_visible

    @pytest.mark.parametrize(
        "pos, expected_score",
        [
            ((2, 1), 4),
            ((2, 3), 8),
            ((3, 4), 0),
        ],
    )
    def test_compute_scenic_score(self, pos, expected_score):
        # Prepare
        height_map = parsed_data.copy()

        # Run
        actual_score = day8.compute_scenic_score(height_map, pos)

        # Assert
        assert expected_score == actual_score

    def test_get_max_scenic_score(self):
        # Prepare
        height_map = parsed_data.copy()
        expected_max_score = 8

        # Run
        actual_max_score = day8.get_max_scenic_score(height_map)

        # Assert
        assert expected_max_score == actual_max_score
