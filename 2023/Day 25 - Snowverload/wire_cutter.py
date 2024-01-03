#!/usr/bin/env python3
import networkx as nx
from math import prod

# Using max-flow min-cuts theorem:
# https://en.wikipedia.org/wiki/Max-flow_min-cut_theorem
# The maximum amount of flow created in a graph
# from a source to a sink is the minimum
# weight of the cuts that we need to make
# to separate out nodes, and create two disjointed graphs
# set our weights to 1 to get the number of specific cuts
#
# The nx package appears to use the Dinic's algorithm.
# https://www.hackerearth.com/practice/algorithms/graphs/maximum-flow/tutorial/
# Figure out the maximal flow. THe edges that experience their own flow max
# are the ones that are cut to create the two disjoints.
def handle_input(input: str) -> dict[str, list[str]]:
    f = open(input, "r")
    lines = f.read().split("\n")
    f.close()
    g = dict()
    for line in lines:
        left, right = line.strip().split(": ")
        g[left] = [part for part in right.split(" ")]
    return g


def get_graph(g_dict: dict[str, list[str]]):
    graph = nx.Graph(g_dict)
    nx.set_edge_attributes(graph, 1.0, "capacity")
    return graph

def get_disjoint_partitions(graph: nx.Graph, cuts: int) -> tuple[set[str], set[str]]:
    source = next(iter(graph.nodes))
    for sink in graph.nodes:
        if source != sink:
            cut_val, partitions = nx.minimum_cut(graph, source, sink)
            if cut_val == cuts:
                return partitions
    return 

if __name__ == "__main__":
    g_dict = handle_input("puzzle input.txt")
    graph = get_graph(g_dict)
    partitions = get_disjoint_partitions(graph, 3)
    print(f"Part 1: {prod(len(partition) for partition in partitions)}")
    print("Part 2: You supply all fifty stars and restart global snow production!")
