from src.aoc2022.days import day2
from src.aoc2022.days.day2 import Move, Strategy

LOSE_PTS = 0
DRAW_PTS = 3
WIN_PTS = 6

ROCK_PTS = 1
PAPER_PTS = 2
SCISSORS_PTS = 3

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

point_mappings_moves = {
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

point_mappings_strategy = {
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


class TestDay2:
    def test_move_strategy(self):
        # Prepare
        raw_input = """
        A Y
        B X
        C Z
        """
        expected_points = 15

        # Run
        data = day2.parse_data(raw_input, move_mapping, move_mapping)
        actual_points = day2.calculate_points(data, point_mappings_moves)

        # assert
        assert actual_points == expected_points

    def test_correct_strategy(self):
        # Prepare
        raw_input = """
        A Y
        B X
        C Z
        """
        expected_points = 12

        # Run
        data = day2.parse_data(raw_input, move_mapping, strategy_mapping)
        actual_points = day2.calculate_points(data, point_mappings_strategy)

        # assert
        assert actual_points == expected_points
