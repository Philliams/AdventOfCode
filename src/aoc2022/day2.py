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


class Move(Enum):
    """
    Enum for valid Rock-Paper-Scissors game
    """

    ROCK = "Rock"
    """
    Value for 'Rock' move.
    """
    PAPER = "Paper"
    """
    Value for 'Paper' move.
    """
    SCISSORS = "Scissors"
    """
    Value for 'Scissors' move.
    """


class Strategy(Enum):
    """
    Enum for valid Rock-Paper-Scissors game
    """

    # Human-readable strategies
    LOSE = "lose"
    """
    Value for 'lose' strategy.
    """
    DRAW = "draw"
    """
    Value for 'draw' strategy.
    """
    WIN = "win"
    """
    Value for 'win' strategy.
    """


WIN_POINTS = 6
TIE_POINTS = 3
LOSE_POINTS = 0
move_points = {Move.ROCK: 1, Move.PAPER: 2, Move.SCISSORS: 3}

# convention is [your_move][their_move]
win_points = {
    Move.ROCK: {
        Move.ROCK: TIE_POINTS,
        Move.PAPER: LOSE_POINTS,
        Move.SCISSORS: WIN_POINTS,
    },
    Move.PAPER: {
        Move.ROCK: WIN_POINTS,
        Move.PAPER: TIE_POINTS,
        Move.SCISSORS: LOSE_POINTS,
    },
    Move.SCISSORS: {
        Move.ROCK: LOSE_POINTS,
        Move.PAPER: WIN_POINTS,
        Move.SCISSORS: TIE_POINTS,
    },
}


def parse_data_naive(raw_data: str) -> List[Tuple[str, str]]:
    """
    Parses the raw text input into lists of tuples of (move, move)

    :param raw_data: Raw text data to be parsed
    :type raw_data: str

    :return: List of move tuples
    :rtype: List[Tuple[Move, Move]]
    """
    raw_data = raw_data.strip()
    rows = raw_data.split("\n")
    values = [row.strip().split(" ") for row in rows]

    parsed_data = []

    for row in values:
        if row[0] == 'A':
            their_move = Move.ROCK
        if row[0] == 'B':
            their_move = Move.PAPER
        if row[0] == 'C':
            their_move = Move.SCISSORS

        if row[1] == 'X':
            your_move = Move.ROCK
        if row[1] == 'Y':
            your_move = Move.PAPER
        if row[1] == 'Z':
            your_move = Move.SCISSORS

        parsed_data.append((their_move, your_move))

    return parsed_data

def parse_data_correct(raw_data: str) -> List[Tuple[str, str]]:
    """
    Parses the raw text input into lists of tuples of (move, strategy)

    :param raw_data: Raw text data to be parsed
    :type raw_data: str

    :return: List of move and strategy tuples
    :rtype: List[Tuple[Move, Strategy]]
    """
    raw_data = raw_data.strip()
    rows = raw_data.split("\n")
    values = [row.strip().split(" ") for row in rows]

    parsed_data = []

    for row in values:
        if row[0] == 'A':
            their_move = Move.ROCK
        if row[0] == 'B':
            their_move = Move.PAPER
        if row[0] == 'C':
            their_move = Move.SCISSORS

        if row[1] == 'X':
            your_strat = Strategy.LOSE
        if row[1] == 'Y':
            your_strat = Strategy.DRAW
        if row[1] == 'Z':
            your_strat = Strategy.WIN

        result = (their_move, your_strat)

        parsed_data.append(result)

    return parsed_data


def get_move(their_move: Move, your_strat: Strategy) -> Move:
    """
    Computes needed move given their move and your strategy

    :param their_move: The opponent's move
    :type their_move: Move

    :param your_strat: The strategy for this round (win/draw/lose)
    :type your_strat: Strategy

    :return: The move you should play
    :rtype: Move
    """
    points = win_points[their_move]

    if your_strat.value == Strategy.LOSE.value:
        return max(points, key=points.get)
    elif your_strat.value == Strategy.DRAW.value:
        return their_move
    else:
        return min(points, key=points.get)


def get_points(their_move: Move, your_move: Move) -> int:
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


def get_game_points_naive(strategy_guide: List[Tuple[Move, Move]]) -> int:
    """
    Computes the total number of points following the naive strategy guide

    :param strategy_guide: List of all round moves
    :type strategy_guide: List[Tuple[Move, Move]]

    :return: Total score
    :rtype: int
    """

    score = 0

    for their_move, your_move in strategy_guide:
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
        your_move = get_move(their_move, your_strat)
        score += get_points(their_move, your_move)

    return score


if __name__ == "__main__":  # pragma: no cover
    raw_data = get_raw_data(file_path="./data/day2.txt")
    parsed_data = parse_data_naive(raw_data)
    total_points = get_game_points_naive(parsed_data)

    print(f"You got {total_points} using the naive strategy.")

    parsed_data = parse_data_correct(raw_data)
    total_points = get_game_points_correct(parsed_data)

    print(f"You got {total_points} using the correct strategy.")
