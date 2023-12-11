#!/usr/bin/env python3
import re


def get_graph(nodes: str) -> dict[str, dict[str, str]]:
    return {
        m[0]: {"L": m[1], "R": m[2]}
        for m in [re.findall(r"[A-Z]{3}", node) for node in nodes.split("\n")]
    }


def find_req_steps(input: str) -> int:
    f = open(input, "r")
    directions, nodes = f.read().split("\n\n")
    graph = get_graph(nodes)
    steps = 0
    i = 0
    current_node = "AAA"
    while current_node != "ZZZ":
        direction = directions[i]
        current_node = graph[current_node][direction]
        steps += 1
        i = (i + 1) % len(directions)
    return steps

if __name__ == "__main__":
    print(f"Part 1: {find_req_steps('puzzle input.txt')}")