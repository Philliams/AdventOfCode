from typing import List, Tuple


def get_raw_data(file_path: str = None) -> str:
    """Returns the raw data from a path (or example if path is None)

    :param file_path: filepath for data
    :type file_path: str

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

    if file_path is None:
        return raw_data
    else:
        with open(file_path, "r") as file:
            data = file.read()
        return data


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
    max_value = -1  # smallest since all integers are guaranteed positive
    for idx, group in enumerate(groups):
        sum_ = sum(group)
        if sum_ > max_value:
            max_idx = idx
            max_value = sum_

    return max_idx, max_value


def get_3_largest_group_sum(groups: List[List[int]]) -> List[Tuple[int, int]]:
    """Finds the 3 top group with the largests sums

    :param groups: A list of groups, where each group is a list of integers
    :type groups: List[List[int]]

    :return: Index of the 3 groups with the largests sums + corresponding sums
    :rtype: List[Tuple[int, int]]
    """

    top_val = -1  # smallest since all integers are guaranteed positive
    top_idx = 0

    mid_val = -1  # smallest since all integers are guaranteed positive
    mid_idx = 0

    bot_val = -1  # smallest since all integers are guaranteed positive
    bot_idx = 0

    for idx, group in enumerate(groups):
        sum_ = sum(group)
        if sum_ <= bot_val:
            pass
        elif (sum_ > bot_val) and (sum_ <= mid_val):
            bot_val = sum_
            bot_idx = idx
        elif (sum_ > mid_val) and (sum_ <= top_val):
            bot_val = mid_val
            bot_idx = mid_idx

            mid_val = sum_
            mid_idx = idx
        else:
            bot_val = mid_val
            bot_idx = mid_idx

            mid_val = top_val
            mid_idx = top_idx

            top_val = sum_
            top_idx = idx

    return [(bot_idx, bot_val), (mid_idx, mid_val), (top_idx, top_val)]


if __name__ == "__main__":  # pragma: no cover
    data = get_raw_data(file_path="./data/day1.txt")
    parsed_data = parse_data_to_array(data)
    idx, sum_ = get_largest_group_sum(parsed_data)
    print(
        f"The elf carrying most calories is #{idx+1}"
        f" with a total of {sum_} calories"
    )

    top_groups = get_3_largest_group_sum(parsed_data)
    top_calories = sum([t[1] for t in top_groups])
    print(f"The top 3 elves are carrying {top_calories} calories")
