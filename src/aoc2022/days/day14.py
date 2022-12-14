from typing import Tuple

import numpy as np

from src.aoc2022 import utils


def parse_data_to_array(
    raw_data: str, starting_point: Tuple[int, int]
) -> Tuple[np.ndarray, Tuple[int, int]]:
    """
    Parse raw data into a grid of air/stone cells

    :param raw_data: Raw data to parse into packets
    :type raw_data: str

    :param starting_point: Starting point from where sand is dropped
    :type starting_point: Tuple[int, int]

    :return: the generated map and updated starting point
    :rtype: Tuple[np.ndarray, Tuple[int, int]]
    """
    min_x_value = starting_point[0]
    min_y_value = starting_point[1]
    max_x_value = starting_point[0]
    max_y_value = starting_point[1]
    paths = []

    for line in raw_data.split("\n"):
        coords = line.split(" -> ")
        path = []
        for i in range(len(coords)):
            x, y = coords[i].split(",")

            x_val = int(x)
            y_val = int(y)

            min_x_value = min(x_val, min_x_value)
            max_x_value = max(x_val, max_x_value)
            min_y_value = min(y_val, min_y_value)
            max_y_value = max(y_val, max_y_value)

            path.append((x_val, y_val))

        paths.append(path)

    shape = (max_x_value - min_x_value + 1, max_y_value - min_y_value + 1)
    map_ = np.zeros(shape)

    normalized_starting_point = (
        starting_point[0] - min_x_value,
        starting_point[1] - min_y_value,
    )

    for path in paths:
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]

            x1 = min(path[i][0], path[i + 1][0])
            y1 = min(path[i][1], path[i + 1][1])
            x2 = max(path[i][0], path[i + 1][0])
            y2 = max(path[i][1], path[i + 1][1])

            x1 = x1 - min_x_value
            x2 = x2 - min_x_value

            y1 = y1 - min_y_value
            y2 = y2 - min_y_value

            if x1 != x2:
                x2 += 1
                map_[x1:x2, y1] = 1
            elif y1 != y2:
                y2 += 1
                map_[x1, y1:y2] = 1

    return map_, normalized_starting_point


def add_floor_to_map(
    map_: np.ndarray, starting_point: Tuple[int, int]
) -> Tuple[np.ndarray, Tuple[int, int]]:
    """
    Add a floor underneath the given map

    :param map_: The map to which the extra floor is added
    :type map_: np.ndarray

    :param starting_point: Starting point from where sand is dropped
    :type starting_point: Tuple[int, int]

    :return: the updated map and starting point
    :rtype: Tuple[np.ndarray, Tuple[int, int]]
    """
    # want starting point to be in middle, need to find size of new map
    height = map_.shape[1] + 2
    width = 2 * height + map_.shape[0]

    copy_left = height
    copy_right = height + map_.shape[0]
    copy_top = 0
    copy_bot = map_.shape[1]

    new_map = np.zeros((width, height))
    new_map[copy_left:copy_right, copy_top:copy_bot] = map_
    new_map[:, -1] = 1

    new_starting_point = (starting_point[0] + height, 0)

    return new_map, new_starting_point


def simulate_grain_of_sand(
    map_: np.ndarray, starting_point: Tuple[int, int]
) -> Tuple[int, int]:
    """
    Simulate a grain of sand falling through the map

    :param map_: The map through which the grain of sand falls
    :type map_: np.ndarray

    :param starting_point: Starting point from where sand is dropped
    :type starting_point: Tuple[int, int]

    :return: The updated cell that the grain of sand falls onto
    :rtype: Tuple[int, int]
    """
    x, y = starting_point
    max_x, max_y = map_.shape
    while (x >= 0) and (x < max_x) and (y >= 0) and (y < max_y - 1):
        if map_[x, y] != 0:
            return (-1, -1)
        if map_[x, y + 1] == 0:
            y += 1
        else:
            if map_[x - 1, y + 1] == 0:
                x -= 1
                y += 1
            elif map_[x + 1, y + 1] == 0:
                x += 1
                y += 1
            else:
                return (x, y)
    return (-1, -1)


def render_map(map_: np.ndarray, start_point: Tuple[int, int]) -> str:
    """
    Render the map for visualization

    :param map_: The map through which the grain of sand falls
    :type map_: np.ndarray

    :param starting_point: Starting point from where sand is dropped
    :type starting_point: Tuple[int, int]

    :return: A rendered representation of the map
    :rtype: str
    """
    render = np.full(map_.shape, "")
    render[map_ == 0] = "."
    render[map_ == 1] = "#"
    render[map_ == 2] = "o"
    render[start_point] = "S"

    return "\n".join(["".join(render[:, i]) for i in range(render.shape[1])])


def simulate_sand_falling(
    map_: np.ndarray, starting_point: Tuple[int, int]
) -> np.ndarray:
    """
    Repeatedly drop grains of sand til convergence

    :param map_: The map through which the grain of sand falls
    :type map_: np.ndarray

    :param starting_point: Starting point from where sand is dropped
    :type starting_point: Tuple[int, int]

    :return: converged map state after grain of sand fall off edge of map
    :rtype: np.ndarray
    """
    map_ = map_.copy()
    updated_point = simulate_grain_of_sand(map_, starting_point)

    while updated_point != (-1, -1):
        map_[updated_point] = 2
        updated_point = simulate_grain_of_sand(map_, starting_point)
    return map_


if __name__ == "__main__":  # pragma: no cover

    starting_point = (500, 0)
    verbose = False

    raw_data = utils.get_raw_data("./src/aoc2022/data/day14.txt")
    map_, new_start = parse_data_to_array(raw_data, starting_point)

    sand_filled_map = simulate_sand_falling(map_, new_start)

    print(f"{sand_filled_map[sand_filled_map == 2].shape[0]} grains fell")

    if verbose:
        print("Before :")
        print(render_map(map_, new_start))
        print("After :")
        print(render_map(sand_filled_map, new_start))

    map_with_floor, start_with_floor = add_floor_to_map(map_, new_start)
    sand_filled_map = simulate_sand_falling(map_with_floor, start_with_floor)

    print(f"{sand_filled_map[sand_filled_map == 2].shape[0]} grains fell")

    if verbose:
        print("Before :")
        print(render_map(map_with_floor, start_with_floor))
        print("After :")
        print(render_map(sand_filled_map, start_with_floor))
