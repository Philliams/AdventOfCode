from enum import Enum
from typing import Dict, List, Tuple, Union

from src.aoc2022.utils import get_raw_data


class Move(Enum):
    """
    Enum for valid Rock-Paper-Scissors game
    """

    ROCK = 1
    """
    Value for 'Rock' move.
    """
    PAPER = 2
    """
    Value for 'Paper' move.
    """
    SCISSORS = 3
    """
    Value for 'Scissors' move.
    """


class Strategy(Enum):
    """
    Enum for valid strategies
    """

    LOSE = 1
    """
    Value for 'Lose' strategy.
    """
    DRAW = 2
    """
    Value for 'Draw' strategy.
    """
    WIN = 3
    """
    Value for 'Win' strategy.
    """


union_dict_type = Union[Dict[str, Move], Dict[str, Strategy]]


def parse_data(
    raw_data: str,
    l_mapping: Dict[str, Move],
    r_mapping: union_dict_type,
) -> List[Tuple[int, int]]:
    """
    Parses the raw text input into lists of tuples of (Enum, Enum)

    :param raw_data: Raw text data to be parsed
    :type raw_data: str

    :param l_mapping: Mapping to convert string to enum value
    :type l_mapping:

    :param r_mapping: Mapping to convert string to enum value
    :type r_mapping:

    :return: List of parsed tuples
    :rtype: List[Tuple[Enum, Enum]]
    """
    raw_data = raw_data.strip()
    rows = raw_data.split("\n")
    values = [row.strip().split(" ") for row in rows]

    parsed_data = []
    for left_token, right_token in values:
        l_val = l_mapping[left_token].value
        r_val = r_mapping[right_token].value
        parsed_row = (l_val, r_val)
        parsed_data.append(parsed_row)

    return parsed_data


def calculate_points(
    rounds: List[Tuple[int, int]],
    pts_mapping: Dict[Tuple[int, int], int],
) -> int:
    """
    Calculates the number of points given a list of rounds and a point mapping

    :param rounds: List of tuples for each round
    :type rounds: List[Tuple[Enum, Enum]]

    :param pts_mapping: Mapping to convert a round to a point count
    :type pts_mapping: Dict[str, Enum]

    :return: Total score across all rounds
    :rtype: int
    """
    values: List[int] = [int(pts_mapping[round_]) for round_ in rounds]
    return sum(values)


if __name__ == "__main__":  # pragma: no cover
    move_mapping: Dict[str, Move] = {
        "A": Move.ROCK,
        "B": Move.PAPER,
        "C": Move.SCISSORS,
        "X": Move.ROCK,
        "Y": Move.PAPER,
        "Z": Move.SCISSORS,
    }

    strategy_mapping: Dict[str, Strategy] = {
        "X": Strategy.LOSE,
        "Y": Strategy.DRAW,
        "Z": Strategy.WIN,
    }

    LOSE_PTS = 0
    DRAW_PTS = 3
    WIN_PTS = 6

    ROCK_PTS = 1
    PAPER_PTS = 2
    SCISSORS_PTS = 3

    point_mappings_part_1: Dict[Tuple[int, int], int] = {
        (Move.ROCK.value, Move.ROCK.value): ROCK_PTS + DRAW_PTS,
        (Move.PAPER.value, Move.ROCK.value): ROCK_PTS + LOSE_PTS,
        (Move.SCISSORS.value, Move.ROCK.value): ROCK_PTS + WIN_PTS,
        (Move.ROCK.value, Move.PAPER.value): PAPER_PTS + WIN_PTS,
        (Move.PAPER.value, Move.PAPER.value): PAPER_PTS + DRAW_PTS,
        (Move.SCISSORS.value, Move.PAPER.value): PAPER_PTS + LOSE_PTS,
        (Move.ROCK.value, Move.SCISSORS.value): SCISSORS_PTS + LOSE_PTS,
        (Move.PAPER.value, Move.SCISSORS.value): SCISSORS_PTS + WIN_PTS,
        (Move.SCISSORS.value, Move.SCISSORS.value): SCISSORS_PTS + DRAW_PTS,
    }

    point_mappings_part_2: Dict[Tuple[int, int], int] = {
        (Move.ROCK.value, Strategy.LOSE.value): SCISSORS_PTS + LOSE_PTS,
        (Move.PAPER.value, Strategy.LOSE.value): ROCK_PTS + LOSE_PTS,
        (Move.SCISSORS.value, Strategy.LOSE.value): PAPER_PTS + LOSE_PTS,
        (Move.ROCK.value, Strategy.DRAW.value): ROCK_PTS + DRAW_PTS,
        (Move.PAPER.value, Strategy.DRAW.value): PAPER_PTS + DRAW_PTS,
        (Move.SCISSORS.value, Strategy.DRAW.value): SCISSORS_PTS + DRAW_PTS,
        (Move.ROCK.value, Strategy.WIN.value): PAPER_PTS + WIN_PTS,
        (Move.PAPER.value, Strategy.WIN.value): SCISSORS_PTS + WIN_PTS,
        (Move.SCISSORS.value, Strategy.WIN.value): ROCK_PTS + WIN_PTS,
    }

    raw_data = get_raw_data(file_path="./src/aoc2022/data/day2.txt")

    parsed_data = parse_data(raw_data, move_mapping, move_mapping)
    total_points = calculate_points(parsed_data, point_mappings_part_1)

    print(f"You got {total_points} using the naive strategy.")

    parsed_data = parse_data(raw_data, move_mapping, strategy_mapping)
    total_points = calculate_points(parsed_data, point_mappings_part_2)

    print(f"You got {total_points} using the correct strategy.")
