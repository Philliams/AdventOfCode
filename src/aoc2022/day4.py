from typing import List, Tuple

def get_raw_data(file_path: str = None) -> str:
    """Returns the raw data from a path (or example if path is None)

    :param file_path: filepath for data
    :type file_path: str

    :return: Raw text input for example
    :rtype: str
    """
    raw_data = """
        2-4,6-8
        2-3,4-5
        5-7,7-9
        2-8,3-7
        6-6,4-6
        2-6,4-8
        """

    if file_path is None:
        return raw_data
    else:
        with open(file_path, "r") as file:
            data = file.read()
        return data

def parse_data_to_array(raw_data: str) -> List[Tuple[int]]:
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
        first_start, first_end = first_pair.split("-")
        second_start, second_end = second_pair.split("-")

        parsed_data.append((int(first_start), int(first_end), int(second_start), int(second_end)))

    return parsed_data


def set_contains_other_set(ranges: Tuple[int]) -> bool:
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

def set_overlaps(ranges: Tuple[int]) -> bool:
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
    data = get_raw_data("./data/day4.txt")
    parsed_data = parse_data_to_array(data)

    containing_sets = [set_contains_other_set(sets) for sets in parsed_data]
    containing_count = sum(containing_sets)

    print(f"{containing_count} pairs have a set contained by the other.")

    overlapping_sets = [set_overlaps(sets) for sets in parsed_data]
    overlapping_count = sum(overlapping_sets)

    print(f"{overlapping_count} pairs overlap.")
