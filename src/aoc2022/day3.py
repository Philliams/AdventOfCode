from typing import List


def get_raw_data(file_path: str = None) -> str:
    """Returns the raw data from a path (or example if path is None)

    :param file_path: filepath for data
    :type file_path: str

    :return: Raw text input for example
    :rtype: str
    """
    raw_data = """
        vJrwpWtwJgWrhcsFMMfFFhFp
        jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
        PmmdzqPrVvPwwTWBwg
        wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
        ttgJtRGJQctTZtZT
        CrZsJsPPZsGzwwsLwLmpwMDw
        """

    if file_path is None:
        return raw_data
    else:
        with open(file_path, "r") as file:
            data = file.read()
        return data


def item_priority(char: str) -> int:
    """Get the priority value for a character

    :param char: the character to convert to a priority value
    :type char: str

    :return: Priority value
    :rtype: int
    """
    if char.isupper():
        return (ord(char) - 65) + 27
    else:
        return (ord(char) - 97) + 1


def parse_data_to_array(raw_data: str) -> List[List[int]]:
    """
    Parses the raw text input into lists of priority values

    :param raw_data: Raw text data to be parsed
    :type raw_data: str

    :return: Parsed list of lists values
    :rtype: List[List[int]]
    """
    lines = raw_data.replace(" ", "").strip().split("\n")

    priority_values = [[item_priority(c) for c in line] for line in lines]

    parsed_data = []
    for line in lines:
        priority_values = [item_priority(c) for c in line]

        parsed_data.append(priority_values)

    return parsed_data


def get_shared_element(left_list: List[int], right_list: List[int]) -> int:
    """
    Get the shared element between the two lists

    :param left_list: left list of items
    :type left_list: List[int]

    :param right_list: right list of items
    :type right_list: List[int]

    :return: shared element between lists
    :rtype: int
    """
    left_list = sorted(left_list)
    right_list = sorted(right_list)

    idx = 0
    idy = 0

    while left_list[idx] != right_list[idy]:
        if left_list[idx] < right_list[idy]:
            idx += 1
        elif left_list[idx] > right_list[idy]:
            idy += 1

    return left_list[idx]


def count_total_priority(items: List[List[int]]) -> int:
    """
    Count the total priority for the 2 compartment case

    :param items: list of all backpack contents
    :type items: List[List[int]]

    :return: total sum of priority for the shared items
    :rtype: int
    """
    sum_ = 0
    for priorities in items:

        n = len(priorities) // 2

        left_list = priorities[:n]
        right_list = priorities[n:]
        sum_ += get_shared_element(left_list, right_list)
    return sum_


def get_triplet_shared_element(
    left_list: List[int], middle_list: List[int], right_list: List[int]
) -> int:
    """
    Get the shared element between the three lists

    :param left_list: left list of items
    :type left_list: List[int]

    :param middle_list: left list of items
    :type middle_list: List[int]

    :param right_list: right list of items
    :type right_list: List[int]

    :return: shared element between lists
    :rtype: int
    """
    l_list = sorted(left_list)
    m_list = sorted(middle_list)
    r_list = sorted(right_list)

    idx = 0
    idy = 0
    idz = 0

    while not (l_list[idx] == m_list[idy] == r_list[idz]):
        if (l_list[idx] <= m_list[idy]) and (l_list[idx] <= r_list[idz]):
            idx += 1
        elif (m_list[idy] <= l_list[idx]) and (m_list[idy] <= r_list[idz]):
            idy += 1
        else:
            idz += 1

    return l_list[idx]


def count_triplet_priority(items: List[List[int]]) -> int:
    """
    Count the total priority for the 3 compartment case

    :param items: list of all backpack contents
    :type items: List[List[int]]

    :return: total sum of priority for the shared items
    :rtype: int
    """

    sum_ = 0
    for i in range(0, len(items), 3):
        left_list = items[i]
        middle_list = items[i + 1]
        right_list = items[i + 2]
        sum_ += get_triplet_shared_element(left_list, middle_list, right_list)
    return sum_


if __name__ == "__main__":  # pragma: no cover
    data = get_raw_data("./data/day3.txt")
    parsed_data = parse_data_to_array(data)

    total_priority = count_total_priority(parsed_data)
    print(f"The incorrect items add up to {total_priority} priority.")

    total_priority = count_triplet_priority(parsed_data)
    print(f"The badges add up to {total_priority} priority.")
