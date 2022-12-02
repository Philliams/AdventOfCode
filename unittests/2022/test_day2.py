from src.aoc2022 import day2

LOSE_PTS = 0
DRAW_PTS = 3
WIN_PTS = 6

ROCK_PTS = 1
PAPER_PTS = 2
SCISSORS_PTS = 3

move_mapping = {
    "A": day2.Move.ROCK,
    "B": day2.Move.PAPER,
    "C": day2.Move.SCISSORS,
    "X": day2.Move.ROCK,
    "Y": day2.Move.PAPER,
    "Z": day2.Move.SCISSORS,
}

strategy_mapping = {
    "X": day2.Strategy.LOSE,
    "Y": day2.Strategy.DRAW,
    "Z": day2.Strategy.WIN,
}

point_mappings_moves = {
    (day2.Move.ROCK, day2.Move.ROCK): ROCK_PTS + DRAW_PTS,
    (day2.Move.PAPER, day2.Move.ROCK): ROCK_PTS + LOSE_PTS,
    (day2.Move.SCISSORS, day2.Move.ROCK): ROCK_PTS + WIN_PTS,
    (day2.Move.ROCK, day2.Move.PAPER): PAPER_PTS + WIN_PTS,
    (day2.Move.PAPER, day2.Move.PAPER): PAPER_PTS + DRAW_PTS,
    (day2.Move.SCISSORS, day2.Move.PAPER): PAPER_PTS + LOSE_PTS,
    (day2.Move.ROCK, day2.Move.SCISSORS): SCISSORS_PTS + LOSE_PTS,
    (day2.Move.PAPER, day2.Move.SCISSORS): SCISSORS_PTS + WIN_PTS,
    (day2.Move.SCISSORS, day2.Move.SCISSORS): SCISSORS_PTS + DRAW_PTS,
}

point_mappings_strategy = {
    (day2.Move.ROCK, day2.Strategy.LOSE): SCISSORS_PTS + LOSE_PTS,
    (day2.Move.PAPER, day2.Strategy.LOSE): ROCK_PTS + LOSE_PTS,
    (day2.Move.SCISSORS, day2.Strategy.LOSE): PAPER_PTS + LOSE_PTS,
    (day2.Move.ROCK, day2.Strategy.DRAW): ROCK_PTS + DRAW_PTS,
    (day2.Move.PAPER, day2.Strategy.DRAW): PAPER_PTS + DRAW_PTS,
    (day2.Move.SCISSORS, day2.Strategy.DRAW): SCISSORS_PTS + DRAW_PTS,
    (day2.Move.ROCK, day2.Strategy.WIN): PAPER_PTS + WIN_PTS,
    (day2.Move.PAPER, day2.Strategy.WIN): SCISSORS_PTS + WIN_PTS,
    (day2.Move.SCISSORS, day2.Strategy.WIN): ROCK_PTS + WIN_PTS,
}


class TestDay1:
    def test_move_strategy(self):
        # Prepare
        raw_input = day2.get_raw_data()
        expected_points = 15

        # Run
        data = day2.parse_data(raw_input, move_mapping, move_mapping)
        actual_points = day2.calculate_points(data, point_mappings_moves)

        # assert
        assert actual_points == expected_points

    def test_correct_strategy(self):
        # Prepare
        raw_input = day2.get_raw_data()
        expected_points = 12

        # Run
        data = day2.parse_data(raw_input, move_mapping, strategy_mapping)
        actual_points = day2.calculate_points(data, point_mappings_strategy)

        # assert
        assert actual_points == expected_points
