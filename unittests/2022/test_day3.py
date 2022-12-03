from src.aoc2022 import day3

import random
import hypothesis.strategies as st
from hypothesis import given

list_size = st.integers(min_value=1, max_value=10)
random_integer = st.integers(min_value=-100_000, max_value=100_000)

random.seed(1234)

@st.composite
def lists_with_shared_element(draw):
    n = draw(list_size)

    set_generator = st.sets(random_integer, min_size = (3 * n) + 1, max_size= (3 * n) + 1)
    disjoint_values = draw(set_generator)

    shared_value = disjoint_values.pop()
    left_values = [disjoint_values.pop() for _ in range(n)] + [shared_value]
    middle_values = [disjoint_values.pop() for _ in range(n)] + [shared_value]
    right_values = [disjoint_values.pop() for _ in range(n)] + [shared_value]

    random.shuffle(left_values)
    random.shuffle(middle_values)
    random.shuffle(right_values)

    return left_values, middle_values, right_values, shared_value
    

class TestDay3:

    def test_item_priority(self):
        # Assert
        assert day3.item_priority("a") == 1
        assert day3.item_priority("z") == 26
        assert day3.item_priority("A") == 27
        assert day3.item_priority("Z") == 52

    @given(lists_with_shared_element())
    def test_get_shared_element(self, lists_with_shared_element):
        # Prepare
        left_list, _, right_list, expected_common_value = lists_with_shared_element

        # Run
        common_element = day3.get_shared_element(left_list, right_list)

        # Assert
        assert common_element == expected_common_value

    @given(lists_with_shared_element())
    def test_get_triplet_shared_element(self, lists_with_shared_element):
        # Prepare
        left_list, middle_list, right_list, expected_common_value = lists_with_shared_element

        # Run
        common_element = day3.get_triplet_shared_element(left_list, middle_list, right_list)

        # Assert
        assert common_element == expected_common_value


    def test_count_total_priority(self):
        # Prepare
        raw_input = day3.get_raw_data()
        parsed_data = day3.parse_data_to_array(raw_input)
        expected_priority = 157

        # Run
        actual_priority = day3.count_total_priority(parsed_data)

        # assert
        assert actual_priority == expected_priority

    def test_count_triplet_priority(self):
        # Prepare
        raw_input = day3.get_raw_data()
        parsed_data = day3.parse_data_to_array(raw_input)
        expected_priority = 70

        # Run
        actual_priority = day3.count_triplet_priority(parsed_data)

        # assert
        assert actual_priority == expected_priority
