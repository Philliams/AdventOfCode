from src.aoc2022 import utils


def detect_start_of_packet(sequence: str, num_distinct: int) -> int:
    """
    Identifies the position of the starting packet defined by num_distinct
    consecutive unique characters

    :param sequence: Sequence of characters to detect the start packet
    :type sequence: str

    :param num_distinct: Number of consecutive distinct characters needed
    :type num_distinct: int

    :return: Position of the end of the starting packet
    :rtype: int
    """
    for i in range(num_distinct - 1, len(sequence)):
        offset = i - num_distinct
        vals = sequence[offset:i]
        if len(set(vals)) == num_distinct:
            return i
    return -1


if __name__ == "__main__":  # pragma: no cover
    data = utils.get_raw_data("./src/aoc2022/data/day6.txt")

    res = detect_start_of_packet(data, 4)

    print(f"Start of packet found after {res} chars.")

    res = detect_start_of_packet(data, 14)

    print(f"Start of packet found after {res} chars.")
