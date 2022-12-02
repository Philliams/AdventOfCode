import hypothesis.strategies as st
from hypothesis import given

from src.aoc2022 import day2

valid_their_moves = st.sampled_from(["A", "B", "C"])
valid_your_moves = st.sampled_from(["X", "Y", "Z"])

class TestDay1:
    def test_parse_data(self):
        # Prepare
        raw_input = day2.get_raw_data()

        # Run
        actual = day2.parse_data_to_array(raw_input)
        expected = [
            ["A", "Y"],
            ["B", "X"],
            ["C", "Z"]
        ]

        # Assert
        assert actual == expected

    def test_get_points(self):
        # Prepare
        rock = day2.ValidMove.ROCK
        paper = day2.ValidMove.PAPER
        scissors = day2.ValidMove.SCISSORS

        rock_pts = 1
        paper_pts = 2
        scissors_pts = 3

        win_pts = 6
        tie_pts = 3
        lose_pts = 0

        # Run/Assert

        assert day2.get_points(rock, scissors) == scissors_pts + lose_pts
        assert day2.get_points(paper, scissors) == scissors_pts + win_pts
        assert day2.get_points(scissors, scissors) == scissors_pts + tie_pts

        assert day2.get_points(rock, paper) == paper_pts + win_pts
        assert day2.get_points(paper, paper) == paper_pts + tie_pts
        assert day2.get_points(scissors, paper) == paper_pts + lose_pts

        assert day2.get_points(rock, rock) == rock_pts + tie_pts
        assert day2.get_points(paper, rock) == rock_pts + lose_pts
        assert day2.get_points(scissors, rock) == rock_pts + win_pts

    def test_get_move(self):
        rock = day2.ValidMove.ROCK
        paper = day2.ValidMove.PAPER
        scissors = day2.ValidMove.SCISSORS

        move_points = {
            rock: 1,
            paper: 2,
            scissors: 3,
        }

        lose = day2.Strategy.LOSE
        draw = day2.Strategy.DRAW
        win = day2.Strategy.WIN

        rock_pts = 1
        paper_pts = 2
        scissors_pts = 3

        win_pts = 6
        tie_pts = 3
        lose_pts = 0

        strat_points = [lose_pts, tie_pts, win_pts]

        for i, move in enumerate([rock, paper, scissors]):
            for j, strat in enumerate([lose, draw, win]):
                your_move = day2.get_move(move, strat)
                assert day2.get_points(move, your_move) == move_points[your_move] + strat_points[j]

    def test_naive_strategy(self):
        # Prepare
        raw_input = day2.get_raw_data()
        parsed_input = day2.parse_data_to_array(raw_input)
        expected_pts = 15

        # Run
        actual_pts = day2.get_game_points_naive(parsed_input)

        # assert
        assert actual_pts == expected_pts

    def test_correct_strategy(self):
        # Prepare
        raw_input = day2.get_raw_data()
        parsed_input = day2.parse_data_to_array(raw_input)
        expected_pts = 12

        # Run
        actual_pts = day2.get_game_points_correct(parsed_input)

        # assert
        assert actual_pts == expected_pts


        