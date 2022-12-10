import pytest

from src.aoc2022 import utils
from src.aoc2022.days import day10


class TestDay10:
    def test_parse_data(self):
        # Prepare
        input_data = "noop\nnoop\naddx 5"
        expected_parsed = [["noop"], ["noop"], ["addx", "5"]]
        # Run
        actual_parsed = day10.parse_data_to_array(input_data)

        # Assert
        assert expected_parsed == actual_parsed

    def test_simulate_cpu_state_machine(self):
        # Prepare
        input_instructions = [["noop"], ["addx", "3"], ["addx", "-5"]]
        expected_states = [
            (1, 1),
            (2, 1),
            (3, 1),
            (4, 4),
            (5, 4),
        ]

        # Run
        cpu_simulator = day10.simulate_cpu_state_machine(input_instructions)
        actual_states = [(cycle, value) for cycle, value in cpu_simulator]

        # Assert
        assert actual_states == expected_states

    def test_simulate_cpu_state_machine_invalid_input(self):
        # Prepare
        input_instructions = [
            ["some_invalid_value"],
        ]
        expected_error = "Invalid CPU instruction ['some_invalid_value']"

        # Run
        cpu_simulator = day10.simulate_cpu_state_machine(input_instructions)
        with pytest.raises(ValueError) as exc_info:
            [(cycle, value) for cycle, value in cpu_simulator]

        # Assert
        assert str(exc_info.value) == expected_error

    def test_get_total_signal_strength(self):
        # Prepare
        test_data_path = "./unittests/2022/test_data/day10_sample.txt"
        input_data = utils.get_raw_data(test_data_path)
        input_instructions = day10.parse_data_to_array(input_data)
        expected_sum = 13140

        # Run
        actual_sum = day10.get_total_signal_strength(input_instructions)

        # Assert
        assert expected_sum == actual_sum

    def test_render_cpu_pixel_values(self):
        # Prepare
        test_data_path = "./unittests/2022/test_data/day10_sample.txt"
        input_data = utils.get_raw_data(test_data_path)
        input_instructions = day10.parse_data_to_array(input_data)
        expected_render = (
            "##..##..##..##..##..##..##..##..##..##..\n"
            "###...###...###...###...###...###...###.\n"
            "####....####....####....####....####....\n"
            "#####.....#####.....#####.....#####.....\n"
            "######......######......######......####\n"
            "#######.......#######.......#######....."
        )

        # Run
        actual_render = day10.render_cpu_pixel_values(input_instructions)

        # Assert
        assert actual_render == expected_render
