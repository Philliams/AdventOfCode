import hypothesis.strategies as st
from hypothesis import given

from src.aoc2022 import day1

non_neg_integer = st.integers(min_value=0, max_value=100_000)
integer_list = st.lists(non_neg_integer, min_size=1, max_size=1024)
list_of_lists = st.lists(integer_list, min_size=3, max_size=64)


class TestDay1:
    def test_parse_data(self):
        # Prepare
        raw_input = day1.get_raw_data()

        # Run
        actual = day1.parse_data_to_array(raw_input)
        expected = [
            [1000, 2000, 3000],
            [4000],
            [5000, 6000],
            [7000, 8000, 9000],
            [10_000],
        ]

        # Assert
        assert actual == expected

    def test_example_based_get_largest_group_sum(self):
        # Prepare
        input_data = [
            [1000, 2000, 3000],
            [4000],
            [5000, 6000],
            [7000, 8000, 9000],
            [10_000],
        ]

        # Run
        actual_idx, actual_sum = day1.get_largest_group_sum(input_data)

        # Assert
        assert actual_sum == 24_000
        assert actual_idx == 3

    @given(list_of_lists)  # property-based testing
    def test_property_based_get_largest_group_sum(self, groups):
        # prepare
        sums = [sum(group) for group in groups]
        max_ = max(sums)

        # Run
        actual_idx, actual_sum = day1.get_largest_group_sum(groups)

        # Assert
        assert actual_sum == max_
        assert actual_idx >= 0
        if len(groups) > 0:
            assert actual_idx < len(groups)

    @given(list_of_lists)  # property-based testing
    def test_propert_based_get_3_largest_group_sums(self, groups):
        # prepare
        sums = [sum(group) for group in groups]
        sorted_sums = sorted(sums)

        # Run
        top_groups = day1.get_3_largest_group_sum(groups)

        # Assert
        assert top_groups[0][1] == sorted_sums[-3]  # 3rd largest
        assert top_groups[1][1] == sorted_sums[-2]  # 2nd largest
        assert top_groups[2][1] == sorted_sums[-1]  # largest
