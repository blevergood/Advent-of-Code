#!/usr/bin/env python3
class Tile:
    def __init__(self, val: str, x: int, y: int) -> None:
        self.val = val
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"{self.val}, ({self.x}, {self.y})"

    def __repr__(self) -> str:
        return str(self)


def handle_input(input: str) -> (list[list[Tile]], Tile):
    f = open(input, "r")
    grid_str = f.read().split("\n")
    f.close()
    grid = []
    start = None
    end = None
    for y in range(len(grid_str)):
        row = []
        for x in range(len(grid_str[y])):
            tile = Tile(grid_str[y][x], x, y)
            if start is None and tile.val == ".":
                start = tile
            if y == len(grid_str) - 1 and end is None and tile.val == ".":
                end = tile
            row.append(tile)
        grid.append(row)
    return grid, start, end


def valid_tile(grid: list[list[Tile]], x: int, y: int) -> bool:
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid) and grid[y][x].val != "#"


# Get all the tiles that have more than 2 directions.
# Used to compress the map so we can do less DFS recursion.
# If a tile only has two directions, we can only move forward, so we can just
# just jump to the next vertex where we actually to make a decision.
def get_vertices(
    grid: list[list[Tile]], directions: dict[str, list[tuple[int, int]]]
) -> set[Tile]:
    vertices = set()
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if tile.val != "#":
                neighbors = []
                for x, y in directions["."]:
                    next_x = tile.x + x
                    next_y = tile.y + y
                    if valid_tile(grid, next_x, next_y):
                        neighbors.append(grid[next_y][next_x])
                if len(neighbors) > 2:
                    vertices.add(tile)
    return vertices


# https://github.com/derailed-dash/Advent-of-Code/blob/master/src/AoC_2023/Dazbo's_Advent_of_Code_2023.ipynb
def build_edges(
    grid: list[list[Tile]],
    directions: dict[str, list[tuple[int, int]]],
    vertices: set[Tile],
    part_one: bool = True,
) -> dict[Tile, set[Tile]]:
    edges = {vertex: set() for vertex in vertices}
    for vertex in vertices:
        queue = [(vertex, 0)]
        visited = []
        while len(queue) > 0:
            tile, distance = queue.pop(0)
            if tile not in visited:
                visited.append(tile)
                # Go straight in a given direction until we find another vertex
                # OR we find a tile that keeps us from moving in that same direction
                for x, y in directions["."]:
                    next_x = tile.x + x
                    next_y = tile.y + y
                    if valid_tile(grid, next_x, next_y):
                        if (
                            grid[next_y][next_x] in vertices
                            and grid[next_y][next_x] != vertex
                        ):
                            edges[vertex].add((grid[next_y][next_x], distance + 1))
                            continue
                        if part_one:
                            if grid[next_y][next_x].val != "." and directions[
                                grid[next_y][next_x].val
                            ] != [(x, y)]:
                                continue
                        queue.append((grid[next_y][next_x], distance + 1))
    return edges


# Idea from: https://www.reddit.com/r/adventofcode/comments/18oy4pc/comment/kgf4iy9/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
def direct_perimeter(
    edges: dict[Tile, set[Tile]], start: Tile
) -> dict[Tile, set[Tile]]:
    visited = set()
    queue = [start]
    while len(queue) > 0:
        tile = queue.pop(0)
        for path in edges[tile]:
            if len(edges[path[0]]) < 4 and path[0] not in visited:
                to_remove = set()
                queue.append(path[0])
                for p in edges[path[0]]:
                    if tile in p:
                        to_remove.add(p)
                        break
                edges[path[0]] -= to_remove
        visited.add(tile)
    return edges


def get_paths(
    current: Tile,
    end: Tile,
    grid: list[list[Tile]],
    edges: dict[Tile, set[Tile, int]],
    visited: set[Tile] = set(),
) -> list[int]:
    if current == end:
        return [0]
    visited.add(current)
    path_lengths = []
    for next_vertex, distance in edges[current]:
        if next_vertex not in visited:
            for path_length in get_paths(next_vertex, end, grid, edges, visited):
                path_lengths.append(path_length + distance)
    visited.remove(current)
    return path_lengths


# Fun little utility function to create visualizations like from the problem statement
# To help when I got stuck with my graph traversal
# Doesn't work with the current vertex-jumping algorithm
def visualize(input: str, all_paths: list[list[Tile]]) -> None:
    f = open(input, "r")
    lines = f.readlines()
    f.close()

    line = list(lines[start.y])
    line[start.x] = "S"
    s = "".join(line)
    lines[start.y] = s

    for path in all_paths:
        current_lines = [line for line in lines]
        for tile in path:
            if tile != start:
                line = list(current_lines[tile.y])
                line[tile.x] = "O"
                s = "".join(line)
                current_lines[tile.y] = s
        f = open(f"visualization_{len(path)}.txt", "w+")
        f.writelines(lines)


if __name__ == "__main__":
    directions = {
        ".": [(0, 1), (1, 0), (0, -1), (-1, 0)],
        "^": [(0, -1)],
        ">": [(1, 0)],
        "v": [(0, 1)],
        "<": [(-1, 0)],
    }
    grid, start, end = handle_input("puzzle input.txt")
    vertices = get_vertices(grid, directions)
    vertices.add(start)
    vertices.add(end)
    edges = build_edges(grid, directions, vertices)
    path_lengths = get_paths(start, end, grid, edges)
    print(f"Part 1: {max(path_lengths)}")

    p2_edges = direct_perimeter(
        build_edges(grid, directions, vertices, part_one=False), start
    )
    p2_lengths = get_paths(start, end, grid, p2_edges, set())
    print(f"Part 2: {max(p2_lengths)}")
