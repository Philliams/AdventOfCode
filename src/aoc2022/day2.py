from enum import Enum
from typing import Dict, List, Tuple


def get_raw_data(file_path: str = None) -> str:
    """Returns the raw data from a path (or example if path is None)

    :param file_path: filepath for data
    :type file_path: str

    :return: Raw text input for example
    :rtype: str
    """
    raw_data = """
        A Y
        B X
        C Z
        """

    if file_path is None:
        return raw_data
    else:
        with open(file_path, "r") as file:
            data = file.read()
        return data


def parse_data(
    raw_data: str, l_mapping: Dict[str, Enum], r_mapping: Dict[str, Enum]
) -> List[Tuple[Enum, Enum]]:
    """
    Parses the raw text input into lists of tuples of (Enum, Enum)

    :param raw_data: Raw text data to be parsed
    :type raw_data: str

    :param l_mapping: Mapping to convert string to enum value
    :type l_mapping: Dict[str, Enum]

    :param r_mapping: Mapping to convert string to enum value
    :type r_mapping: Dict[str, Enum]

    :return: List of parsed tuples
    :rtype: List[Tuple[Enum, Enum]]
    """
    raw_data = raw_data.strip()
    rows = raw_data.split("\n")
    values = [row.strip().split(" ") for row in rows]

    parsed_data = []
    for left_token, right_token in values:
        parsed_row = (l_mapping[left_token], r_mapping[right_token])
        parsed_data.append(parsed_row)

    return parsed_data


def calculate_points(
    rounds: List[Tuple[Enum, Enum]], pts_mapping: Dict[Tuple[Enum, Enum], int]
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
    return sum([pts_mapping[round_] for round_ in rounds])


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


if __name__ == "__main__":  # pragma: no cover
    move_mapping = {
        "A": Move.ROCK,
        "B": Move.PAPER,
        "C": Move.SCISSORS,
        "X": Move.ROCK,
        "Y": Move.PAPER,
        "Z": Move.SCISSORS,
    }

    strategy_mapping = {
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

    point_mappings_part_1 = {
        (Move.ROCK, Move.ROCK): ROCK_PTS + DRAW_PTS,
        (Move.PAPER, Move.ROCK): ROCK_PTS + LOSE_PTS,
        (Move.SCISSORS, Move.ROCK): ROCK_PTS + WIN_PTS,
        (Move.ROCK, Move.PAPER): PAPER_PTS + WIN_PTS,
        (Move.PAPER, Move.PAPER): PAPER_PTS + DRAW_PTS,
        (Move.SCISSORS, Move.PAPER): PAPER_PTS + LOSE_PTS,
        (Move.ROCK, Move.SCISSORS): SCISSORS_PTS + LOSE_PTS,
        (Move.PAPER, Move.SCISSORS): SCISSORS_PTS + WIN_PTS,
        (Move.SCISSORS, Move.SCISSORS): SCISSORS_PTS + DRAW_PTS,
    }

    point_mappings_part_2 = {
        (Move.ROCK, Strategy.LOSE): SCISSORS_PTS + LOSE_PTS,
        (Move.PAPER, Strategy.LOSE): ROCK_PTS + LOSE_PTS,
        (Move.SCISSORS, Strategy.LOSE): PAPER_PTS + LOSE_PTS,
        (Move.ROCK, Strategy.DRAW): ROCK_PTS + DRAW_PTS,
        (Move.PAPER, Strategy.DRAW): PAPER_PTS + DRAW_PTS,
        (Move.SCISSORS, Strategy.DRAW): SCISSORS_PTS + DRAW_PTS,
        (Move.ROCK, Strategy.WIN): PAPER_PTS + WIN_PTS,
        (Move.PAPER, Strategy.WIN): SCISSORS_PTS + WIN_PTS,
        (Move.SCISSORS, Strategy.WIN): ROCK_PTS + WIN_PTS,
    }

    raw_data = get_raw_data(file_path="./data/day2.txt")

    parsed_data = parse_data(raw_data, move_mapping, move_mapping)
    total_points = calculate_points(parsed_data, point_mappings_part_1)

    print(f"You got {total_points} using the naive strategy.")

    parsed_data = parse_data(raw_data, move_mapping, strategy_mapping)
    total_points = calculate_points(parsed_data, point_mappings_part_2)

    print(f"You got {total_points} using the correct strategy.")
