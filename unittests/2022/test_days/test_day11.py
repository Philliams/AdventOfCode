from src.aoc2022 import utils
from src.aoc2022.days import day11


class TestDay11:
    def test_parse_monkeys(self):
        # Prepare
        test_data_path = "./unittests/2022/test_data/day11_sample.txt"
        input_data = utils.get_raw_data(test_data_path)

        def assert_monkeys_equal(m1, m2):
            assert m1.items == m2.items
            assert m1.divisible == m2.divisible
            assert m1.true_throw == m2.true_throw
            assert m1.false_throw == m2.false_throw

            for i in range(10):
                assert m1.operation(i) == m2.operation(i)

        expected_monkeys = {
            0: day11.Monkey(
                items=[79, 98],
                operation=lambda x: x * 19,
                divisible=23,
                true_throw=2,
                false_throw=3,
            ),
            1: day11.Monkey(
                items=[54, 65, 75, 74],
                operation=lambda x: x + 6,
                divisible=19,
                true_throw=2,
                false_throw=0,
            ),
            2: day11.Monkey(
                items=[79, 60, 97],
                operation=lambda x: x**2,
                divisible=13,
                true_throw=1,
                false_throw=3,
            ),
            3: day11.Monkey(
                items=[74],
                operation=lambda x: x + 3,
                divisible=17,
                true_throw=0,
                false_throw=1,
            ),
        }

        # Run
        actual_monkeys = day11.parse_data_to_dict(input_data)

        # Assert
        assert expected_monkeys.keys() == actual_monkeys.keys()
        for k in expected_monkeys.keys():
            assert_monkeys_equal(expected_monkeys[k], actual_monkeys[k])

    def test_monkey_game_with_div(self):
        # Prepare
        test_data_path = "./unittests/2022/test_data/day11_sample.txt"
        input_data = utils.get_raw_data(test_data_path)
        monkeys = day11.parse_data_to_dict(input_data)

        n_rounds = 20

        expected_res = {0: 101, 1: 95, 2: 7, 3: 105}

        # Run
        actual_res = day11.compute_number_of_counted_items(n_rounds, monkeys)

        # Assert
        assert expected_res == actual_res

    def test_monkey_game_with_no_div(self):
        # Prepare
        test_data_path = "./unittests/2022/test_data/day11_sample.txt"
        input_data = utils.get_raw_data(test_data_path)
        input_monkeys = day11.parse_data_to_dict(input_data)

        num_rounds = 10_000

        expected_counts = {0: 52166, 1: 47830, 2: 1938, 3: 52013}

        # Run
        actual_counts = day11.compute_number_of_counted_items_no_div(
            num_rounds, input_monkeys
        )

        # Assert
        assert expected_counts == actual_counts

    def test_parse_monkeys_additional_operation(self):
        # Prepare
        input_data = """Monkey 3:
  Starting items: 74
  Operation: new = old + old
  Test: divisible by 1
    If true: throw to monkey 0
    If false: throw to monkey 1"""

        # Run
        parsed_monkey = day11.parse_block(input_data)

        # Assert
        assert parsed_monkey.items == [74]
        assert parsed_monkey.divisible == 1
        assert parsed_monkey.true_throw == 0
        assert parsed_monkey.false_throw == 1
        for i in range(10):
            assert parsed_monkey.operation(i) == i + i
