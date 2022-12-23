import itertools
from typing import Dict, Generator, List, Optional, Set, Tuple

from src.aoc2022 import utils


class Graph:
    """
    Data class representing a graph of nodes and edges

    :param flow_rates: A dict of node name, flow rate
    :type flow_rates: Dict[str, int]

    :param cons: a dict of node name, node edges
    :type cons: Dict[str, List[str]]
    """

    def __init__(self, flow_rates: Dict[str, int], cons: Dict[str, List[str]]):
        self.flow_rates = flow_rates
        self.valves = sorted(list(self.flow_rates.keys()))
        self.connections = cons
        self.distance_matrix = {}
        for node in flow_rates.keys():
            distances = self.compute_distance_matrix(node)
            self.distance_matrix[node] = distances

    def get_valves(self) -> List[str]:
        """
        Get a list of all valve names

        :return: valve names
        :rtype: List[str]
        """
        return self.valves

    def get_connections(self, node_name: str) -> List[str]:
        """
        Get connections for a specified node

        :param node_name: Name of node to retrieve connections
        :type node_name: str

        :return: the names of the connected nodes for the given node
        :rtype: List[str]
        """
        return self.connections[node_name]

    def get_flow_rate(self, node_name) -> int:
        """
        Get flow rate for a specified node

        :param node_name: Name of node to retrieve flow rate
        :type node_name: str

        :return: Flow rate of given node
        :rtype: int
        """
        return self.flow_rates[node_name]

    def get_flow_rates(self) -> Dict[str, int]:
        """
        Get flow rates for all nodes

        :return: Dict of node name, flow rate
        :rtype: Dict[str, int]
        """
        return self.flow_rates

    def get_minimal_distance(self, start: str, end: str) -> int:
        """
        Get shortest distance between two valves

        :param start: Name of starting node
        :type start: str

        :param node_name: Name of end node
        :type node_name: str

        :return: shortest distance between both nodes
        :rtype: int
        """
        return self.distance_matrix[start][end]

    def compute_distance_matrix(self, start: str) -> Dict[str, int]:
        """
        Compute shortest distance from starting node to all other nodes

        :param start: Name of starting node
        :type start: str

        :return: shortest distance from starting node to all other nodes
        :rtype: Dict[str, int]
        """
        distances = {start: 0}

        stack = [start]
        visited = set()

        while stack:
            node = stack.pop(0)
            if node not in visited:
                visited.add(node)
                for neighbour in self.get_connections(node):
                    stack.append(neighbour)
                    increment_dist = distances[node] + 1
                    default_dist = distances.get(neighbour, increment_dist)
                    distances[neighbour] = min(default_dist, increment_dist)

        return distances

    def time_aware_permutations(
        self, position: str, remaining_valves: Set[str], remaining_time: int
    ) -> Generator[List[Tuple[str, int]], None, None]:
        """
        Generate all possible permutations of valve openings that respect
        the time limits

        :param position: Name of current node
        :type position: str

        :param remaining_valves: valves that have not yet been opened
        :type remaining_valves: Set[str]

        :param remaining_time: Amount of time remaining before eruption
        :type remaining_time: int

        :return: shortest distance from starting node to all other nodes
        :rtype: Dict[str, int]
        """
        if (remaining_time <= 0) or (len(remaining_valves) == 0):
            yield [(position, max(remaining_time, 0))]
        else:
            for new_pos in remaining_valves:
                valves = remaining_valves.copy()
                valves.remove(new_pos)

                dist = self.get_minimal_distance(position, new_pos)

                updated_time = remaining_time - dist - 1

                for subsearch in self.time_aware_permutations(
                    new_pos, valves, updated_time
                ):
                    yield [(position, remaining_time)] + subsearch


def parse_data_to_graph(raw_data: str) -> Graph:
    """
    Parse raw data into a Graph of valves and connections

    :param raw_data: Raw data to parse into Graph
    :type raw_data: str

    :return: the parsed Graph data
    :rtype: Graph
    """

    connections = {}
    flow_rates = {}

    for line in raw_data.split("\n"):
        flow_rate_str, connection_str = line.split("; ")

        valve_name_str, flow_rate_str = flow_rate_str.split("rate=")
        flow_rate = int(flow_rate_str)
        valve_name = valve_name_str.split(" ")[1]

        connection_str = connection_str.replace("valves", "valve")
        valve_connections = connection_str.split("valve ")[-1].split(", ")

        flow_rates[valve_name] = flow_rate
        connections[valve_name] = valve_connections

    return Graph(flow_rates, connections)


def get_optimal_sequence(
    graph: Graph,
    start: str,
    total_time: int,
    non_zero_valves: Optional[List[str]] = None,
) -> Tuple[List[Tuple[str, int]], int]:
    """
    Compute the optimal valve opening sequence

    :param graph: Graph of valves to open
    :type graph: Graph

    :param start: Name of starting node
    :type start: str

    :param total_time: total time for valve sequence
    :type total_time: int

    :param non_zero_valves: Optional list of valves to specify for search
    :type non_zero_valves: Optional[List[str]]

    :return: Optimal sequence and score for opening valves
    :rtype: Tuple[List[Tuple[str, int]], int]
    """
    if non_zero_valves is None:
        valves = graph.get_flow_rates()
        non_zero_valves = [k for k, v in valves.items() if v > 0]

    max_ = 0
    max_path = []

    search_valves = set(non_zero_valves)
    paths = graph.time_aware_permutations(start, search_valves, total_time)

    for path in paths:

        score = sum([v * graph.get_flow_rate(k) for k, v in path])

        if score > max_:
            max_ = score
            max_path = path

    return max_path, max_


def get_optimal_dual_sequence(
    graph: Graph, start: str, total_time: int
) -> Tuple[List[Tuple[str, int]], List[Tuple[str, int]], int]:
    """
    Compute the optimal valve opening sequence for two agents

    :param graph: Graph of valves to open
    :type graph: Graph

    :param start: Name of starting node
    :type start: str

    :param total_time: total time for valve sequence
    :type total_time: int

    :return: Optimal paths for elephant and person, and associated score
    :rtype: Tuple[List[Tuple[str, int]], List[Tuple[str, int]], int]
    """
    real_valves = [k for k, v in graph.get_flow_rates().items() if v > 0]
    n = len(real_valves)

    optimal_cache: Dict[frozenset, Tuple] = {}

    max_ = 0
    path_type = List[Tuple[str, int]]
    max_paths: Tuple[path_type, path_type] = ([], [])

    partition_flag_combinations = itertools.product([True, False], repeat=n)
    for idx, bool_flags in enumerate(partition_flag_combinations):

        elephant_valves = [real_valves[i] for i in range(n) if bool_flags[i]]
        person_valves = [real_valves[i] for i in range(n) if not bool_flags[i]]

        elephant_cache_valves = frozenset(elephant_valves)
        person_cache_valves = frozenset(person_valves)

        e_score = 0
        p_score = 0

        if elephant_cache_valves in optimal_cache:
            e_path, e_score = optimal_cache[elephant_cache_valves]
        else:
            e_path, e_score = get_optimal_sequence(
                graph, start, total_time, non_zero_valves=elephant_valves
            )
            optimal_cache[elephant_cache_valves] = (e_path, e_score)

        if person_cache_valves in optimal_cache:
            p_path, p_score = optimal_cache[person_cache_valves]
        else:
            p_path, p_score = get_optimal_sequence(
                graph, start, total_time, non_zero_valves=person_valves
            )
            optimal_cache[person_cache_valves] = (p_path, p_score)

        combined_score = p_score + e_score

        if combined_score > max_:
            max_ = combined_score
            max_paths = (e_path, p_path)

    return *max_paths, max_


if __name__ == "__main__":  # pragma: no cover

    raw_data = utils.get_raw_data("./src/aoc2022/data/day16.txt")
    graph = parse_data_to_graph(raw_data)
    start_node = "AA"
    total_time = 30

    path, score = get_optimal_sequence(graph, start_node, total_time)

    print(f"The best path is {path} which will release {score} pressure")

    total_time = 26
    _, _, score = get_optimal_dual_sequence(graph, start_node, total_time)

    print(f"The best path will release {score} pressure")
