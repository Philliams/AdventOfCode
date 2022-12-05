import hypothesis.strategies as st
from hypothesis import given

from src.aoc2022.days import day4

range_size = st.integers(min_value=0, max_value=1_000)
random_integer = st.integers(min_value=-100_000, max_value=100_000)


@st.composite
def random_containing_set(draw):
    size_1 = draw(range_size)
    size_2 = draw(range_size)

    outer_size = max(size_1, size_2)
    inner_size = min(size_1, size_2)

    anchor = draw(random_integer)
    offset = draw(st.integers(min_value=0, max_value=outer_size - inner_size))

    left_start = anchor
    left_end = left_start + inner_size
    right_start = anchor - offset
    right_end = right_start + outer_size

    return (left_start, left_end, right_start, right_end)


@st.composite
def random_non_overlapping(draw):

    size_1 = draw(range_size)
    size_2 = draw(range_size)

    disjoint_size = draw(st.integers(min_value=1, max_value=1_000))

    anchor = draw(random_integer)

    return (
        anchor - size_1,
        anchor,
        anchor + disjoint_size,
        anchor + disjoint_size + size_2,
    )


@st.composite
def random_overlapping_set(draw):
    size_1 = draw(range_size)
    size_2 = draw(range_size)

    overlap_strategy = st.integers(min_value=0, max_value=min(size_1, size_2))
    overlap_size = draw(overlap_strategy)

    anchor = draw(random_integer)

    return (
        anchor - size_1,
        anchor,
        anchor - overlap_size,
        anchor - overlap_size + size_2,
    )


class TestDay4:
    def test_parse_data(self):
        # Prepare
        raw_input = """
        2-4,6-8
        2-3,4-5
        5-7,7-9
        2-8,3-7
        6-6,4-6
        2-6,4-8
        """

        # Run
        actual = day4.parse_data_to_array(raw_input)
        expected = [
            (2, 4, 6, 8),
            (2, 3, 4, 5),
            (5, 7, 7, 9),
            (2, 8, 3, 7),
            (6, 6, 4, 6),
            (2, 6, 4, 8),
        ]

        # Assert
        assert actual == expected

    @given(random_containing_set())
    def test_set_contains_other_set(self, random_containing_set):
        # Prepare

        # Run
        actual_contains = day4.set_contains_other_set(random_containing_set)

        # Assert
        assert actual_contains

    @given(random_non_overlapping())
    def test_set_contains_non_overlapping(self, random_non_overlapping):
        # Prepare

        # Run
        actual_contains = day4.set_contains_other_set(random_non_overlapping)

        # Assert
        assert not actual_contains

    @given(random_overlapping_set())
    def test_set_overlaps(self, random_overlapping_set):
        # Prepare

        # Run
        actual_overlaps = day4.set_overlaps(random_overlapping_set)

        # Assert
        assert actual_overlaps

    @given(random_non_overlapping())
    def test_set_overlaps_non_overlapping(self, random_non_overlapping):
        # Prepare

        # Run
        actual_overlaps = day4.set_overlaps(random_non_overlapping)

        # Assert
        assert not actual_overlaps
