from typing import Set, Tuple

import numpy as np

from src.aoc2022 import utils


def parse_data_to_array(raw_data: str) -> np.ndarray:
    """
    Parse the raw data into a 2D list of lists

    :param raw_data: Raw data containing numerical data
    :type raw_data: str

    :return: parsed matrix of values
    :rtype: List[List[int]]
    """
    outer_list = []
    for line in raw_data.split("\n"):
        inner_list = [int(e) for e in line]
        outer_list.append(inner_list)

    return np.array(outer_list)


def scan_height_row(height_map: np.ndarray) -> Set[int]:
    """
    Scan a list of heights to determine which trees are visible from either
    side

    :param height_map: 1D array of heights
    :type height_map: np.ndarray

    :return: Set of positions that are visible from either side
    :rtype: Set[int]
    """
    left_max = -1
    right_max = -1
    n = len(height_map)

    visible_positions = set()

    for i in range(n):
        left_idx = i
        right_idx = n - (1 + i)

        left_val = height_map[left_idx]
        right_val = height_map[right_idx]

        if left_val > left_max:
            left_max = left_val
            visible_positions.add(left_idx)
        if right_val > right_max:
            right_max = right_val
            visible_positions.add(right_idx)
    return visible_positions


def count_visible_trees(height_map: np.ndarray) -> int:
    """
    Count number of trees visible from perimeter

    :param height_map: 2D array of heights
    :type height_map: np.ndarray

    :return: Total count of trees visible from perimeter
    :rtype: int
    """
    visible_positions: Set[Tuple[int, int]] = set()

    height, width = height_map.shape

    for row in range(height):
        row_data = height_map[row, :]
        visible_in_row = scan_height_row(row_data)
        for pos in visible_in_row:
            visible_positions.add((row, pos))

    for col in range(width):
        col_data = height_map[:, col]
        visible_in_col = scan_height_row(col_data)
        for pos in visible_in_col:
            visible_positions.add((pos, col))

    return len(visible_positions)


def compute_scenic_score(height_map: np.ndarray, pos: Tuple[int, int]) -> int:
    """
    Compute the scenic view given a starting position

    :param height_map: 2D array of heights
    :type height_map: np.ndarray

    :param pos: tuple of (x, y) positions in the grid
    :type pos: Tuple[int, int]

    :return: Scenic score of the position given
    :rtype: int
    """
    height, width = height_map.shape
    x, y = pos
    start_height = height_map[y, x]

    left_view = 0
    right_view = 0
    top_view = 0
    bot_view = 0

    i = x + 1
    while i < width:
        if height_map[y, i] < start_height:
            right_view += 1
        elif height_map[y, i] >= start_height:
            right_view += 1
            break
        i += 1

    i = x - 1
    while i >= 0:
        if height_map[y, i] < start_height:
            left_view += 1
        elif height_map[y, i] >= start_height:
            left_view += 1
            break
        i -= 1

    j = y + 1
    while j < height:
        if height_map[j, x] < start_height:
            bot_view += 1
        elif height_map[y, x] >= start_height:
            bot_view += 1
            break
        j += 1

    j = y - 1
    while j >= 0:
        if height_map[j, x] < start_height:
            top_view += 1
        elif height_map[y, x] >= start_height:
            top_view += 1
            break
        j -= 1

    return top_view * bot_view * left_view * right_view


def get_max_scenic_score(height_map: np.ndarray) -> int:
    """
    Find the maximum scenic score given the height map

    :param height_map: 2D array of heights
    :type height_map: np.ndarray

    :return: Maximum possible scenic score
    :rtype: int
    """
    max_ = 0
    height, width = height_map.shape
    for x in range(width):
        for y in range(height):
            pos = (x, y)
            view = compute_scenic_score(height_map, pos)
            if view > max_:
                max_ = view
    return max_


if __name__ == "__main__":  # pragma: no cover

    data = utils.get_raw_data("./src/aoc2022/data/day8.txt")

    parsed_array = parse_data_to_array(data)
    vis_trees = count_visible_trees(parsed_array)

    print(f"There are {vis_trees} visible trees.")

    compute_scenic_score(parsed_array, (2, 3))
    max_view = get_max_scenic_score(parsed_array)

    print(f"The best view is {max_view}.")
