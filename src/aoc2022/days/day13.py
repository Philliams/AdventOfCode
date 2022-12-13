from __future__ import annotations

import functools
import json
from typing import List, Tuple, Union

from src.aoc2022 import utils

val_type = Union[List, int]
pack_type = List[val_type]


def parse_data_to_array(raw_data: str) -> List[Tuple[pack_type, pack_type]]:
    """
    Parse raw data into a list of packet tuples

    :param raw_data: Raw data to parse into packets
    :type raw_data: str

    :return: a list of all packet pairs
    :rtype: List[Tuple[List, List]]
    """
    packets = raw_data.split("\n\n")

    packet_pairs = []

    for packet in packets:
        top_packet, bot_packet = packet.split("\n")
        pair = (json.loads(top_packet), json.loads(bot_packet))
        packet_pairs.append(pair)

    return packet_pairs


def element_is_equal(left_val: val_type, right_val: val_type) -> int:
    """
    Perform ternary comparison on two elements. Returns following:
    - 1 if left_val smaller
    - 0 if equal
    - -1 if right_val smaller

    :param left_val: left value for comparison
    :type left_val: element_type

    :param right_val: right value for comparison
    :type right_val: element_type

    :return: Ternary value for equality comparison
    :rtype: int
    """
    if isinstance(left_val, int) and isinstance(right_val, int):
        if left_val < right_val:
            return 1
        elif left_val > right_val:
            return -1
        else:
            return 0
    elif isinstance(left_val, list) and isinstance(right_val, list):

        upper_bound = min(len(left_val), len(right_val))

        for i in range(upper_bound):
            is_eq = element_is_equal(left_val[i], right_val[i])
            if is_eq == 1:
                return 1
            elif is_eq == -1:
                return -1
            else:
                pass

        l_size = len(left_val)
        r_size = len(right_val)

        return element_is_equal(l_size, r_size)

    elif isinstance(left_val, list) and isinstance(right_val, int):
        return element_is_equal(left_val, [right_val])
    else:
        return element_is_equal([left_val], right_val)


def sort_packets(packets: List[pack_type]) -> List[pack_type]:
    """
    Sort packets using comparison function

    :param packets: list of packets to sort
    :type packets: List[pack_type]

    :return: List of sorted packets
    :rtype: List[pack_type]
    """
    packet_ordering_func = functools.cmp_to_key(element_is_equal)
    sorted_packets = sorted(packets, key=packet_ordering_func, reverse=True)

    return sorted_packets


if __name__ == "__main__":  # pragma: no cover

    sample_input = """"""

    raw_data = utils.get_raw_data("./src/aoc2022/data/day13.txt")
    parsed_data = parse_data_to_array(raw_data)

    sum_ = 0

    for i, pair in enumerate(parsed_data):
        left_packet, right_packet = pair
        res = element_is_equal(left_packet, right_packet)
        if res == 1:
            sum_ += i + 1

    print(f"{sum_} pairs are in the correct order")

    divider_packets: List = [[[2]], [[6]]]
    all_packets = divider_packets
    for left_packet, right_packet in parsed_data:
        all_packets.append(left_packet)
        all_packets.append(right_packet)

    sorted_packets = sort_packets(all_packets)

    packet_1_key = sorted_packets.index(divider_packets[0]) + 1
    packet_2_key = sorted_packets.index(divider_packets[1]) + 1

    print(f"The decoder key is {packet_1_key * packet_2_key}")
