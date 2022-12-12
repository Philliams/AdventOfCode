from __future__ import annotations

import math
from typing import Callable, Dict, List, NamedTuple

from src.aoc2022 import utils


class Monkey(NamedTuple):
    """
    Data class representing the monkey configuration

    :param items: list of items the monkey is currently holding
    :type items: List[int]

    :param operation: lambda function for updating the item priority
    :type operation: Callable[[int], int]

    :param divisible: number used for divisible check when throwing items
    :type divisible: int

    :param false_throw: id of monkey to throw to on item % divisible != 0
    :type false_throw: int

    :param true_throw: id of monkey to throw to on item % divisible == 0
    :type true_throw: int

    :return: parsed matrix of values
    :rtype: List[List[str]]
    """

    items: List[int]
    operation: Callable[[int], int]
    divisible: int
    false_throw: int
    true_throw: int

    def add_items(self, items: List[int]):
        """
        Add a list of items to the items held by the monkey

        :param items: List of items to add to the monkey's held items
        :type items: List[int]

        """
        self.items.extend(items)

    def pop_items(self) -> List[int]:
        """
        Pop all the items from the monkey and return the list

        :return: items held by monkey
        :rtype: List[int]
        """
        n = len(self.items)
        return [self.items.pop() for _ in range(n)]

    def copy(self) -> Monkey:
        """
        Create a new copy of this monkey

        :return: Monkey copy
        :rtype: Monkey
        """
        return Monkey(
            items=[e for e in self.items],
            operation=self.operation,
            divisible=self.divisible,
            false_throw=self.false_throw,
            true_throw=self.true_throw,
        )


def parse_data_to_dict(raw_data: str) -> Dict[int, Monkey]:
    """
    Parse the raw data intoa dict of monkeys

    :param raw_data: Raw data containing numerical data
    :type raw_data: str

    :return: parsed dict of Monkey id, Monkey
    :rtype: Dict[int, Monkey]
    """

    parsed_monkeys = {}
    for idx, block in enumerate(raw_data.split("\n\n")):
        monkey = parse_block(block)
        parsed_monkeys[idx] = monkey

    return parsed_monkeys


def parse_block(raw_data_block: str) -> Monkey:
    """
    Parse block of raw data to a single monkey monkey

    :param raw_data_block: Raw data containing data for single monkey
    :type raw_data_block: str

    :return: parsed Monkey instance
    :rtype: Monkey
    """
    lines = raw_data_block.split("\n")

    starting_items_string = lines[1].strip().split(": ")[1]
    starting_items = [int(e) for e in starting_items_string.split(", ")]

    operation_string = lines[2].strip().split(" = ")[-1]
    match operation_string.split(" "):  # noqa
        case ["old", "*", "old"]:  # noqa: E211
            operation = lambda x: x**2  # noqa: E731
        case ["old", "+", "old"]:  # noqa: E211
            operation = lambda x: x + x  # noqa: E731
        case ["old", "*", val]:  # noqa: E211
            value = int(val)  # noqa: F821
            operation = lambda x: x * value  # noqa: E731
        case ["old", "+", val]:  # noqa: E211
            value = int(val)  # noqa: F821
            operation = lambda x: x + value  # noqa: E731

    divisible = int(lines[3].strip().split(" ")[-1])
    true_throw = int(lines[4].strip().split(" ")[-1])
    false_throw = int(lines[5].strip().split(" ")[-1])

    return Monkey(
        items=starting_items,
        operation=operation,
        divisible=divisible,
        false_throw=false_throw,
        true_throw=true_throw,
    )


def compute_number_of_counted_items(
    num_rounds: int, monkeys: Dict[int, Monkey]
) -> Dict[int, int]:
    """
    Compute the number of items each monkey has examined during a game

    :param num_rounds: Number of rounds to simulate
    :type num_rounds: int

    :param monkeys: Monkeys instances to simulate playing the game
    :type monkeys: Dict[int, Monkey]

    :return: Examined items counts for each monkey id
    :rtype: Dict[int, int]
    """

    monkeys = {k: v.copy() for k, v in monkeys.items()}

    n = len(monkeys.keys())

    checked_items = {k: 0 for k in range(n)}

    for i in range(num_rounds):
        for j in range(n):
            monkey = monkeys[j]
            checked_items[j] += len(monkey.items)

            true_throws = []
            false_throws = []

            items = monkey.pop_items()

            for item in items:
                updated_item = monkey.operation(item) // 3

                throw_check = updated_item % monkey.divisible == 0

                if throw_check:
                    true_throws.append(updated_item)
                else:
                    false_throws.append(updated_item)

            monkeys[monkey.false_throw].add_items(false_throws)
            monkeys[monkey.true_throw].add_items(true_throws)

    return checked_items


def compute_number_of_counted_items_no_div(
    num_rounds: int, monkeys: Dict[int, Monkey]
) -> Dict[int, int]:
    """
    Compute the number of items each monkey has examined
    during a game with no division rule

    :param num_rounds: Number of rounds to simulate
    :type num_rounds: int

    :param monkeys: Monkeys instances to simulate playing the game
    :type monkeys: Dict[int, Monkey]

    :return: Examined items counts for each monkey id
    :rtype: Dict[int, int]
    """

    monkeys = {k: v.copy() for k, v in monkeys.items()}

    common_modulo = math.lcm(*[m.divisible for m in monkeys.values()])

    n = len(monkeys.keys())
    checked_items = {k: 0 for k in range(n)}

    for i in range(num_rounds):
        for j in range(n):
            monkey = monkeys[j]
            checked_items[j] += len(monkey.items)

            true_throws = []
            false_throws = []

            items = monkey.pop_items()

            for item in items:
                updated_item = monkey.operation(item) % common_modulo

                throw_check = updated_item % monkey.divisible == 0

                if throw_check:
                    true_throws.append(updated_item)
                else:
                    false_throws.append(updated_item)

            monkeys[monkey.false_throw].add_items(false_throws)
            monkeys[monkey.true_throw].add_items(true_throws)

    return checked_items


if __name__ == "__main__":  # pragma: no cover

    num_rounds = 20

    raw_data = utils.get_raw_data("./src/aoc2022/data/day11.txt")
    parsed_data = parse_data_to_dict(raw_data)

    counted_items = compute_number_of_counted_items(num_rounds, parsed_data)
    sorted_values = sorted(counted_items.values())
    max_mul = sorted_values[-1] * sorted_values[-2]
    print(f"The max priorities multiplied are : {max_mul}")

    num_rounds = 10_000

    res = compute_number_of_counted_items_no_div(num_rounds, parsed_data)
    sorted_values = sorted(res.values())
    max_mul = sorted_values[-1] * sorted_values[-2]
    print(f"The max priorities multiplied are : {max_mul}")
