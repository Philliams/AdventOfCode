from typing import List, Tuple

from src.aoc2022 import utils

stacks_type = Tuple[List[str], ...]
moves_type = List[Tuple[int, int, int]]


def parse_data(raw_data: str) -> Tuple[stacks_type, moves_type]:
    """
    Parses the raw text input into the initial configuration and the move list

    :param raw_data: Raw text data to be parsed
    :type raw_data: str

    :return: Initial Configuration and move list
    :rtype: List[Tuple[int]]
    """
    configuration_data, move_data = raw_data.split("\n\n")

    stack_rows = configuration_data.split("\n")
    reversed_rows = stack_rows[::-1]
    num_stacks = int(reversed_rows[0].split(" ")[-2])

    stacks: Tuple[List[str], ...] = tuple([] for _ in range(num_stacks))

    for row in reversed_rows[1:]:
        values = row[1::4]
        for idx, value in enumerate(values):
            if value != " ":
                stacks[idx].append(value)

    moves = []
    move_lines = move_data.split("\n")
    for move_line in move_lines:
        split_move = move_line.split(" ")
        num_transfer = int(split_move[1])
        start_stack = int(split_move[3])
        end_stack = int(split_move[5])

        moves.append((num_transfer, start_stack, end_stack))

    return stacks, moves


def transfer_items(stacks: stacks_type, moves: moves_type) -> str:
    """
    Computes the final state of the stacks after applying the moves

    :param stacks: Tuple of lists representing each stack
    :type stacks: Tuple[List[str]]

    :param moves: List of tuples for each move
    :type moves: List[Tuple[int]]

    :return: value at the top of each stack after moves
    :rtype: str
    """

    for n, start, stop in moves:
        for _ in range(n):
            v = stacks[start - 1].pop()
            stacks[stop - 1].append(v)

    top_boxes = []
    for s in stacks:
        if len(s) > 0:
            top_boxes.append(s[-1])
        else:
            top_boxes.append(" ")

    return "".join(top_boxes)


def transfer_multiple_items(stacks: stacks_type, moves: moves_type) -> str:
    """
    Computes the final state of the stacks after applying the moves
    moving multiple boxes in a single move

    :param stacks: Tuple of lists representing each stack
    :type stacks: Tuple[List[str]]

    :param moves: List of tuples for each move
    :type moves: List[Tuple[int]]

    :return: value at the top of each stack after moves
    :rtype: str
    """

    for n, start, stop in moves:

        v = stacks[start - 1][-n:]
        for _ in range(n):
            stacks[start - 1].pop()
        stacks[stop - 1].extend(v)

    top_boxes = []
    for s in stacks:
        if len(s) > 0:
            top_boxes.append(s[-1])
        else:
            top_boxes.append(" ")

    return "".join(top_boxes)


if __name__ == "__main__":  # pragma: no cover
    data = utils.get_raw_data("./src/aoc2022/data/day5.txt")
    stacks, moves = parse_data(data)
    result = transfer_items(stacks, moves)
    print(f"The final state of the stacks is {result}")

    stacks, moves = parse_data(data)
    result = transfer_multiple_items(stacks, moves)
    print(f"The final state of the stacks is {result}")
