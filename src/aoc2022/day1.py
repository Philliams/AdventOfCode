from typing import List, Tuple


def get_raw_data() -> str:
    """Returns the raw data for the example case

    :return: Raw text input for example
    :rtype: str
    """
    raw_data = """
        1000
        2000
        3000

        4000

        5000
        6000

        7000
        8000
        9000

        10000
        """
    return raw_data


def parse_data_to_array(raw_data: str) -> List[List[int]]:
    """
    Parses the raw text input into lists of numerical values,
    with one list per grouping of lines

    :param raw_data: Raw text data to be parsed
    :type raw_data: str

    :return: Parsed integer values
    :rtype: List[List[int]]
    """
    raw_data = raw_data.replace(" ", "").strip()
    line_groups = [group for group in raw_data.split("\n\n") if len(group) > 0]

    parsed_data = [[int(e) for e in g.split("\n")] for g in line_groups]

    return parsed_data


def get_largest_group_sum(groups: List[List[int]]) -> Tuple[int, int]:
    """Finds the group with the largest sum

    :param groups: A list of groups, where each group is a list of integers
    :type groups: List[List[int]]

    :return: Index of the group with the largest sum and corresponding sum
    :rtype: Tuple[int, int]
    """

    max_idx = 0
    max_value = 0
    for idx, group in enumerate(groups):
        sum_ = sum(group)
        if sum_ > max_value:
            max_idx = idx
            max_value = sum_

    return max_idx, max_value


if __name__ == "__main__":  # pragma: no cover
    data = get_raw_data()
    parsed_data = parse_data_to_array(data)
    idx, sum_ = get_largest_group_sum(parsed_data)
    print(
        f"The elf carrying most calories is #{idx+1}"
        f" with a total of {sum_} calories"
    )
