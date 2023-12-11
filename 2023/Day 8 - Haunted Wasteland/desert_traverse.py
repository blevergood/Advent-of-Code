#!/usr/bin/env python3
import re
from math import lcm


def get_graph(nodes: str) -> dict[str, dict[str, str]]:
    return {
        m[0]: {"L": m[1], "R": m[2]}
        for m in [re.findall(r"[A-Z]{3}", node) for node in nodes.split("\n")]
    }


def graph_traversal(
    graph: dict[str, dict[str, str]], start, end, directions: str
) -> int:
    steps = 0
    i = 0
    current_node = start
    # Part 1
    if end:
        condition = lambda x: x != "ZZZ"
    # Part 2
    else:
        condition = lambda x: "Z" not in x
    while condition(current_node):
        direction = directions[i]
        current_node = graph[current_node][direction]
        steps += 1
        i = (i + 1) % len(directions)

    return steps


# Part 1
def find_req_steps(input: str) -> int:
    f = open(input, "r")
    directions, nodes = f.read().split("\n\n")
    f.close()
    graph = get_graph(nodes)
    return graph_traversal(graph, "AAA", "ZZZ", directions)


# Part 2
def find_steps_all_exits(input: str) -> int:
    f = open(input, "r")
    directions, nodes = f.read().split("\n\n")
    f.close()
    graph = get_graph(nodes)
    starting_nodes = [node for node in graph.keys() if "A" in node]
    # Find all successful paths independently
    all_paths = [
        graph_traversal(graph, node, "", directions) for node in starting_nodes
    ]

    # Providing the least-common multiple of all paths will give you the first
    # all paths will match up, which is the answer
    return lcm(*all_paths)


if __name__ == "__main__":
    print(f"Part 1: {find_req_steps('puzzle input.txt')}")
    print(f"Part 2: {find_steps_all_exits('puzzle input.txt')}")
