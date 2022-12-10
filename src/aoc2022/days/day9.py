import math
from enum import Enum
from typing import List, Set, Tuple

import numpy as np

from src.aoc2022 import utils


class Move(Enum):
    """
    Enum for valid rope moves
    """

    LEFT = "L"
    """
    Value for 'LEFT' move.
    """
    RIGHT = "R"
    """
    Value for 'RIGHT' move.
    """
    UP = "U"
    """
    Value for 'UP' move.
    """
    DOWN = "D"
    """
    Value for 'DOWN' move.
    """


def parse_data_to_array(raw_data: str) -> List[Tuple[Move, int]]:
    """
    Parse the raw data into a 1D list of move Tuples

    :param raw_data: Raw data containing numerical data
    :type raw_data: str

    :return: parsed matrix of values
    :rtype: List[Tuple[Move, int]]
    """
    parsed_list = []
    for line in raw_data.split("\n"):
        move, count = line.split(" ")
        parsed_list.append((Move(move), int(count)))

    return parsed_list


def get_tail_update(
    head_pos: Tuple[int, int], tail_pos: Tuple[int, int]
) -> Tuple[int, int]:

    x1, y1 = head_pos
    x2, y2 = tail_pos

    L2_distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    if L2_distance >= 2:
        x_move = np.sign(x1 - x2)
        y_move = np.sign(y1 - y2)

        return (x2 + x_move, y2 + y_move)
    else:
        return (x2, y2)


def get_head_update(pos: Tuple[int, int], move: Move) -> Tuple[int, int]:
    x, y = pos

    if move == Move.UP:
        return (x, y + 1)
    elif move == Move.DOWN:
        return (x, y - 1)
    elif move == Move.RIGHT:
        return (x + 1, y)
    else:
        return (x - 1, y)


def get_knot_positions(moves: List[Tuple[Move, int]]) -> Set[Tuple[int, int]]:
    head_pos = (0, 0)
    tail_pos = (0, 0)
    unique_positions = set()

    for move, count in moves:
        for i in range(count):
            head_pos = get_head_update(head_pos, move)
            tail_pos = get_tail_update(head_pos, tail_pos)
            unique_positions.add(tail_pos)

    return unique_positions


def get_multi_knot_positions(
    moves: List[Tuple[Move, int]], num_knots: int
) -> Set[Tuple[int, int]]:
    unique_positions = set()
    knot_positions = [(0, 0) for _ in range(num_knots)]
    for move, count in moves:
        for i in range(count):

            head_pos = knot_positions[0]
            knot_positions[0] = get_head_update(head_pos, move)

            for j in range(num_knots - 1):
                head_pos = knot_positions[j]
                tail_pos = knot_positions[j + 1]
                knot_positions[j + 1] = get_tail_update(head_pos, tail_pos)

            unique_positions.add(knot_positions[-1])

    return unique_positions


if __name__ == "__main__":  # pragma: no cover

    data = utils.get_raw_data("./src/aoc2022/data/day9.txt")

    parsed_array = parse_data_to_array(data)
    unique_positions = get_knot_positions(parsed_array)

    print(f"{len(unique_positions)} unique positions were visited")

    unique_positions = get_multi_knot_positions(parsed_array, 10)

    print(f"{len(unique_positions)} unique positions were visited")
