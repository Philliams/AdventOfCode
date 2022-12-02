from enum import Enum
from typing import List, Tuple


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


WIN_POINTS = 6
TIE_POINTS = 3
LOSE_POINTS = 0


class ValidMove(Enum):
    ROCK = "Rock"
    PAPER = "Paper"
    SCISSORS = "Scissors"


class Strategy(Enum):
    X = "lose"
    Y = "draw"
    Z = "win"

    LOSE = "lose"
    DRAW = "draw"
    WIN = "win"


class PlayerMove(Enum):
    A = ValidMove.ROCK
    B = ValidMove.PAPER
    C = ValidMove.SCISSORS

    X = ValidMove.ROCK
    Y = ValidMove.PAPER
    Z = ValidMove.SCISSORS


move_points = {ValidMove.ROCK: 1, ValidMove.PAPER: 2, ValidMove.SCISSORS: 3}

# convention is [your_move][their_move]
win_points = {
    ValidMove.ROCK: {
        ValidMove.ROCK: TIE_POINTS,
        ValidMove.PAPER: LOSE_POINTS,
        ValidMove.SCISSORS: WIN_POINTS,
    },
    ValidMove.PAPER: {
        ValidMove.ROCK: WIN_POINTS,
        ValidMove.PAPER: TIE_POINTS,
        ValidMove.SCISSORS: LOSE_POINTS,
    },
    ValidMove.SCISSORS: {
        ValidMove.ROCK: LOSE_POINTS,
        ValidMove.PAPER: WIN_POINTS,
        ValidMove.SCISSORS: TIE_POINTS,
    },
}


def parse_data_to_array(raw_data: str) -> List[Tuple[str, str]]:
    """
    Parses the raw text input into lists of tuples

    :param raw_data: Raw text data to be parsed
    :type raw_data: str

    :return: Split string values
    :rtype: List[Tuple[str, str]]
    """
    raw_data = raw_data.strip()
    rows = raw_data.split("\n")
    values = [row.strip().split(" ") for row in rows]

    return values


def get_move(their_move: ValidMove, your_strat: Strategy) -> ValidMove:
    """
    Computes needed move given their move and your strategy

    :param their_move: The opponent's move
    :type their_move: Move

    :param your_strat: The strategy for this round (win/draw/lose)
    :type your_strat: Strategy

    :return: The move you should play
    :rtype: ValidMove
    """
    points = win_points[their_move]

    if your_strat.value == Strategy.LOSE.value:
        return max(points, key=points.get)
    elif your_strat.value == Strategy.DRAW.value:
        return their_move
    else:
        return min(points, key=points.get)


def get_points(their_move: ValidMove, your_move: ValidMove) -> int:
    """
    Computes the number of points given your move and their move

    :param their_move: The opponent's move
    :type their_move: Move

    :param your_move: The player's move
    :type your_move: Move

    :return: Score for round
    :rtype: int
    """

    move_pts = move_points[your_move]
    win_pts = win_points[your_move][their_move]
    return move_pts + win_pts


def get_game_points_naive(strategy_guide: List[Tuple[str, str]]) -> int:
    """
    Computes the total number of points following the naive strategy guide

    :param strategy_guide: List of all round moves
    :type strategy_guide: List[Tuple[str, str]]

    :return: Total score
    :rtype: int
    """

    score = 0

    for their_move, your_move in strategy_guide:
        their_move = PlayerMove[their_move].value
        your_move = PlayerMove[your_move].value

        score += get_points(their_move, your_move)

    return score


def get_game_points_correct(strategy_guide: List[Tuple[str, str]]) -> int:
    """
    Computes the total number of points following the correct strategy guide

    :param strategy_guide: List of all round moves
    :type strategy_guide: List[Tuple[str, str]]

    :return: Total score
    :rtype: int
    """

    score = 0

    for their_move, your_strat in strategy_guide:
        their_move = PlayerMove[their_move].value
        your_strat = Strategy[your_strat]
        your_move = get_move(their_move, your_strat)

        score += get_points(their_move, your_move)

    return score


if __name__ == "__main__":  # pragma: no cover
    raw_data = get_raw_data(file_path="./data/day2.txt")
    parsed_data = parse_data_to_array(raw_data)
    total_points = get_game_points_naive(parsed_data)

    print(f"You got {total_points} using the naive strategy.")

    total_points = get_game_points_correct(parsed_data)

    print(f"You got {total_points} using the correct strategy.")
