from typing import Generator, List, Tuple

from src.aoc2022 import utils


def parse_data_to_array(raw_data: str) -> List[List[str]]:
    """
    Parse the raw data into a 1D list of instruction sets

    :param raw_data: Raw data containing numerical data
    :type raw_data: str

    :return: parsed matrix of values
    :rtype: List[List[str]]
    """
    parsed_list = []
    for line in raw_data.split("\n"):
        instructions = line.split(" ")
        parsed_list.append(instructions)

    return parsed_list


def simulate_cpu_state_machine(
    instructions: List[List[str]],
) -> Generator[Tuple[int, int], None, None]:
    """
    Creates a generator that simulates the CPU on a per-cycle basis

    :param instructions: List of instructions to execute
    :type instructions: List[List[str]]

    :return: per-cycle CPU simulator
    :rtype: Generator[Tuple[int, int], None, None]
    """
    register_value = 1
    cycle = 0

    for instruction_set in instructions:
        match instruction_set:  # noqa
            case ["noop"]:  # noqa: E211
                cycle += 1
                yield (cycle, register_value)
            case ["addx", num]:  # noqa: E211
                value = int(num)  # noqa: F821
                cycle += 1
                yield (cycle, register_value)
                cycle += 1
                yield (cycle, register_value)
                register_value += value
            case _:  # noqa: E211
                raise ValueError(f"Invalid CPU instruction {instruction_set}")


def get_total_signal_strength(instructions: List[List[str]]) -> int:
    """
    Computes the total signal strength as sum of cycle * register value for
    n = 20, 60, 100, 140...

    :param instructions: List of instructions to execute
    :type instructions: List[List[str]]

    :return: total signal strength
    :rtype: int
    """
    running_sum = 0
    cpu_simulator = simulate_cpu_state_machine(instructions)

    for cycle_number, register_value in cpu_simulator:
        if (cycle_number - 20) % 40 == 0:
            running_sum += cycle_number * register_value

    return running_sum


def render_cpu_pixel_values(instructions: List[List[str]]) -> str:
    """
    Render the signal to a simulated console

    :param instructions: List of instructions to execute
    :type instructions: List[List[str]]

    :return: rendered console output
    :rtype: str
    """
    cpu_simulator = simulate_cpu_state_machine(instructions)

    line_width = 40
    render_chars = []
    for cycle_number, register_value in cpu_simulator:
        cursor_pos = (cycle_number - 1) % line_width

        if cursor_pos == 0:
            render_chars.append("\n")

        if abs(register_value - cursor_pos) <= 1:
            render_chars.append("#")
        else:
            render_chars.append(".")

    return "".join(render_chars[1:])  # remove leading newline


if __name__ == "__main__":  # pragma: no cover

    raw_data = utils.get_raw_data("./src/aoc2022/data/day10.txt")

    parsed_data = parse_data_to_array(raw_data)

    res = get_total_signal_strength(parsed_data)

    print(f"The total signal strength is {res}")

    rendered_console = render_cpu_pixel_values(parsed_data)

    print(f"The rendered console is :\n{rendered_console}")
