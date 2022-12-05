from src.aoc2022 import utils


class TestUtils:
    def test_load_file(self):
        # Prepare
        expected_data = (
            "some dummy text\n"
            "another dummy line\n"
            "some dummy numbers\n"
            "1 2 3 4 5\n"
        )
        file_path = "./unittests/2022/test_data/dummy.txt"

        # Run
        actual_data = utils.get_raw_data(file_path)

        # assert
        assert actual_data == expected_data
