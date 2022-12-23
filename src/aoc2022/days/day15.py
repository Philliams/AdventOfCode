from typing import List, Optional, Tuple

from src.aoc2022 import utils


def parse_data_to_array(
    raw_data: str,
) -> List[Tuple[int, int, int, int]]:
    """
    Parse raw data into a list of sensor/closest beacon locations

    :param raw_data: Raw data to parse into sensor/beacon locations
    :type raw_data: str

    :return: the parsed sensor/beacon locations
    :rtype: List[Tuple[int, int]]
    """

    coordinate_pairs = []

    for line in raw_data.split("\n"):
        sensor_str, beacon_str = line.split(": ")

        sensor_prefix = "Sensor at "
        x_str, y_str = sensor_str.replace(sensor_prefix, "").split(", ")
        sensor_location = int(x_str[2:]), int(y_str[2:])

        beacon_prefix = "closest beacon is at "
        x_str, y_str = beacon_str.replace(beacon_prefix, "").split(", ")
        beacon_location = int(x_str[2:]), int(y_str[2:])

        coordinate_pairs.append((*sensor_location, *beacon_location))

    return coordinate_pairs


def count_scanned_location(
    beacon_sensor_locations: List[Tuple[int, int, int, int]],
    row_number: int,
    bounding_range: Optional[Tuple[int, int]] = None,
) -> Tuple[List[Tuple[int, int]], int]:
    """
    Count how many locations have been scanned given the beacon/sensor
    locations and the row number

    :param beacon_sensor_locations: List of sensor/beacon locations
    :type beacon_sensor_locations: List[Tuple[int, int, int, int]]

    :param row_number: The row for which to count the scan locations
    :type row_number: int

    :param bounding_range: an optional bounding range for scan range
    :type bounding_range: Optional[Tuple[int, int]]

    :return: the ranges scanned as well as the total number of scanned cells
    :rtype: Tuple[List[Tuple[int, int]], int]
    """

    ranges = []

    # note this is not optimal, this is O(nm), where n = num beacons, m = size
    # could do an O(n^2) solution by checking each pair of beacons, would be
    # faster in the case that n << m
    for sensor_x, sensor_y, beacon_x, beacon_y in beacon_sensor_locations:

        L1_dist = abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y)

        width = (2 * L1_dist + 1) - (2 * abs(sensor_y - row_number))

        if width > 0:
            left = sensor_x - width // 2
            right = sensor_x + width // 2
            if bounding_range is not None:
                left = max(bounding_range[0], min(bounding_range[1], left))
                right = max(bounding_range[0], min(bounding_range[1], right))

            range_ = (left, right)
            ranges.append(range_)

    potential_beacons = set(
        [t[2] for t in beacon_sensor_locations if t[3] == row_number]
    )

    sorted_ranges = sorted(ranges, key=lambda t: t[0])
    range_stack = [sorted_ranges[0]]

    for start, end in sorted_ranges[1:]:
        stack_start, stack_end = range_stack[-1]

        if stack_start <= start <= stack_end:
            range_stack[-1] = (stack_start, max(stack_end, end))
        else:
            range_stack.append((start, end))

    total_count = 0
    for start, end in range_stack:
        for x in potential_beacons:
            if start <= x <= end:
                total_count -= 1

        total_count += end - start + 1

    return range_stack, total_count


if __name__ == "__main__":  # pragma: no cover

    row_to_analyze = 2_000_000

    raw_data = utils.get_raw_data("./src/aoc2022/data/day15.txt")
    sensor_beacon_coordinates = parse_data_to_array(raw_data)

    ranges, location_count = count_scanned_location(
        sensor_beacon_coordinates, row_to_analyze
    )
    print(f"{location_count} locations are sure to not contain a beacon")

    min_x, max_x = 0, 4_000_000

    for i in range(min_x, max_x):
        ranges, location_count = count_scanned_location(
            sensor_beacon_coordinates, i, bounding_range=(min_x, max_x)
        )

        if len(ranges) != 1:
            x_coord = ranges[0][1] + 1
            print(f"The tuning frequence is {x_coord * 4_000_000 + i}")
            break
