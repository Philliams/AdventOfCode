from src.aoc2022.days import day5


class TestDay5:
    def test_parse_data(self):
        # Prepare
        raw_input = (
            "    [D]    \n"
            "[N] [C]    \n"
            "[Z] [M] [P]\n"
            " 1   2   3 \n\n"
            "move 1 from 2 to 1\n"
            "move 3 from 1 to 3\n"
            "move 2 from 2 to 1\n"
            "move 1 from 1 to 2"
        )

        expected_stacks = (
            ["Z", "N"],
            ["M", "C", "D"],
            ["P"],
        )

        expected_moves = [(1, 2, 1), (3, 1, 3), (2, 2, 1), (1, 1, 2)]

        # Run
        actual_stacks, actual_moves = day5.parse_data(raw_input)

        # Assert
        assert expected_stacks == actual_stacks
        assert expected_moves == actual_moves

    def test_transfer_items(self):
        # Prepare
        stacks = (
            ["Z", "N"],
            ["M", "C", "D"],
            ["P"],
        )

        moves = [(1, 2, 1), (3, 1, 3), (2, 2, 1), (1, 1, 2)]

        expected_state = "CMZ"
        # Run
        actual_state = day5.transfer_items(stacks, moves)

        # Assert
        assert actual_state == expected_state

    def test_transfer_items_empty_stack(self):
        # Prepare
        stacks = (
            ["Z", "N"],
            ["M", "C", "D"],
            ["P"],
        )

        moves = [
            (2, 1, 3),
        ]

        expected_state = " DZ"
        # Run
        actual_state = day5.transfer_items(stacks, moves)

        # Assert
        assert actual_state == expected_state

    def test_transfer_multiple_items(self):
        # Prepare
        stacks = (
            ["Z", "N"],
            ["M", "C", "D"],
            ["P"],
        )

        moves = [(1, 2, 1), (3, 1, 3), (2, 2, 1), (1, 1, 2)]

        expected_state = "MCD"
        # Run
        actual_state = day5.transfer_multiple_items(stacks, moves)

        # Assert
        assert actual_state == expected_state

    def test_transfer_multiple_items_empty_stack(self):
        # Prepare
        stacks = (
            ["Z", "N"],
            ["M", "C", "D"],
            ["P"],
        )

        moves = [
            (2, 1, 3),
        ]

        expected_state = " DN"
        # Run
        actual_state = day5.transfer_multiple_items(stacks, moves)

        # Assert
        assert actual_state == expected_state
