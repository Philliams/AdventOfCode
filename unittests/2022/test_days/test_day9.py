import hypothesis.strategies as st
import pytest
from hypothesis import given

from src.aoc2022.days import day9

seq_size = st.integers(min_value=0, max_value=50)
random_integer = st.integers(min_value=1, max_value=20)
random_move = st.sampled_from(
    [day9.Move.LEFT, day9.Move.RIGHT, day9.Move.UP, day9.Move.DOWN]
)


@st.composite
def generate_random_move_sequence(draw):
    size = draw(seq_size)
    moves = []
    for i in range(size):
        moves.append((draw(random_move), draw(random_integer)))
    return moves


sample_data_small = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

parsed_data_small = [
    (day9.Move.RIGHT, 4),
    (day9.Move.UP, 4),
    (day9.Move.LEFT, 3),
    (day9.Move.DOWN, 1),
    (day9.Move.RIGHT, 4),
    (day9.Move.DOWN, 1),
    (day9.Move.LEFT, 5),
    (day9.Move.RIGHT, 2),
]

sample_data_large = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

parsed_data_large = [
    (day9.Move.RIGHT, 5),
    (day9.Move.UP, 8),
    (day9.Move.LEFT, 8),
    (day9.Move.DOWN, 3),
    (day9.Move.RIGHT, 17),
    (day9.Move.DOWN, 10),
    (day9.Move.LEFT, 25),
    (day9.Move.UP, 20),
]


class TestDay9:
    @pytest.mark.parametrize(
        "input_data, expected_parsed",
        [
            (sample_data_small, parsed_data_small),
            (sample_data_large, parsed_data_large),
        ],
    )
    def test_parse_data(self, input_data, expected_parsed):
        # Prepare

        # Run
        actual_parsed = day9.parse_data_to_array(input_data)

        # Assert
        assert actual_parsed == expected_parsed

    def test_compute_unique_positions(self):
        # Prepare
        move_sequence = parsed_data_small.copy()
        expected_position_count = 13

        # Run
        actual_positions = day9.get_knot_positions(move_sequence)

        # Assert
        assert len(actual_positions) == expected_position_count

    def test_compute_multi_unique_positions(self):
        # Prepare
        moves = parsed_data_large.copy()
        expected_position_count = 36
        num_knots = 10

        # Run
        actual_pos = day9.get_multi_knot_positions(moves, num_knots)

        # Assert
        assert len(actual_pos) == expected_position_count

    @given(generate_random_move_sequence())
    def test_multi_knot_equivalence(self, moves):
        # Prepare
        num_knots = 2

        # Run
        actual_2_pos = day9.get_knot_positions(moves)
        actual_n_pos = day9.get_multi_knot_positions(moves, num_knots)

        # Assert
        assert actual_2_pos == actual_n_pos
