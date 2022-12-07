from typing import List, Tuple

from src.aoc2022.utils import get_raw_data

row_type = Tuple[int, int, int, int]


def parse_data_to_array(raw_data: str) -> List[row_type]:
    """
    Parses the raw text input into lists of value tuples

    :param raw_data: Raw text data to be parsed
    :type raw_data: str

    :return: Parsed list of value tuples
    :rtype: List[Tuple[int]]
    """
    lines = raw_data.replace(" ", "").strip().split("\n")

    parsed_data = []
    for line in lines:

        first_pair, second_pair = line.split(",")
        first_start, first_end = [int(e) for e in first_pair.split("-")]
        second_start, second_end = [int(e) for e in second_pair.split("-")]

        parsed_data.append((first_start, first_end, second_start, second_end))

    return parsed_data


def set_contains_other_set(ranges: row_type) -> bool:
    """
    check whether one of the ranges in entirely contained by the other

    :param ranges: tuple of (start_left, end_left, start_right, end_right)
    :type ranges: Tuple[int]

    :return: flag whether if one set is a subset of the other
    :rtype: bool
    """

    left_start, left_end, right_start, right_end = ranges

    min_cardinality = min(left_end - left_start, right_end - right_start)

    start = max(left_start, right_start)
    end = min(left_end, right_end)

    return (end - start) == min_cardinality


def set_overlaps(ranges: row_type) -> bool:
    """
    check whether the sets overlap at all

    :param ranges: tuple of (start_left, end_left, start_right, end_right)
    :type ranges: Tuple[int]

    :return: flag whether the sets overlap
    :rtype: bool
    """

    left_start, left_end, right_start, right_end = ranges

    start = max(left_start, right_start)
    end = min(left_end, right_end)

    return (end - start) >= 0


if __name__ == "__main__":  # pragma: no cover
    data = get_raw_data("./src/aoc2022/data/day4.txt")
    parsed_data = parse_data_to_array(data)

    containing_sets = [set_contains_other_set(sets) for sets in parsed_data]
    containing_count = sum(containing_sets)

    print(f"{containing_count} pairs have a set contained by the other.")

    overlapping_sets = [set_overlaps(sets) for sets in parsed_data]
    overlapping_count = sum(overlapping_sets)

    print(f"{overlapping_count} pairs overlap.")
