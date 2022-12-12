from typing import Tuple

import numpy as np

from src.aoc2022 import utils


def parse_data_to_array(raw_data: str) -> np.ndarray:
    """
    Parse the raw data into a 1D list of instruction sets

    :param raw_data: Raw data containing numerical data
    :type raw_data: str

    :return: parsed matrix of values
    :rtype: List[List[str]]
    """

    rows = []

    base_value = ord("a")

    start_pos = None
    end_pos = None

    for i, line in enumerate(raw_data.split("\n")):  # row number
        values = []
        for j, char in enumerate(line.strip()):  # col number
            if char == "S":
                values.append(0)
                start_pos = (j, i)
            elif char == "E":
                values.append(ord("z") - base_value)
                end_pos = (j, i)
            else:
                values.append(ord(char) - base_value)
        rows.append(np.array(values))

    return np.array(rows).transpose(), start_pos, end_pos


def get_distance_matrix(data: np.ndarray, pos: Tuple[int, int]) -> np.ndarray:
    """
    Compute the breadth-first distance matrix from aa starting position

    :param data: Height map for the traversal
    :type data: np.ndarray

    :param pos: starting position for the depth-first search
    :type pos: Tuple[int, int]

    :return: the shortest distance from the starting pos to all other points
    :rtype: np.ndarray
    """
    distances = np.full(data.shape, -1)
    distances[pos] = 0
    visited = np.full(data.shape, 0, dtype=bool)

    visit_stack = [pos]

    max_x, max_y = data.shape

    deltas = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ]

    while len(visit_stack) > 0:
        x, y = visit_stack.pop(0)

        if visited[x, y]:
            pass
        else:

            visited[x, y] = True

            for dx, dy in deltas:
                new_x = x + dx
                new_y = y + dy

                valid_x = new_x >= 0 and new_x < max_x
                valid_y = new_y >= 0 and new_y < max_y

                if valid_x and valid_y:

                    valid_pos = data[x, y] - data[new_x, new_y] <= 1

                    if valid_pos and (not visited[new_x, new_y]):
                        distances[new_x, new_y] = distances[x, y] + 1
                        visit_stack.append((new_x, new_y))

    return distances


if __name__ == "__main__":  # pragma: no cover

    raw_data = utils.get_raw_data("./src/aoc2022/data/day12.txt")

    parsed_map, start, end = parse_data_to_array(raw_data)

    distance_matrix = get_distance_matrix(parsed_map, end)
    path_length = distance_matrix[start]

    print(f"The shortest path is {path_length}")

    values = [e for e in distance_matrix[parsed_map == 0] if e != -1]
    closest_start = min(*values)

    print(f"The closest start point is {closest_start}")
