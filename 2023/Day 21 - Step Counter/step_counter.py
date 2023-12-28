#!/usr/bin/env python3
from collections import defaultdict
from collections.abc import Callable
from collections.abc import Generator


def handle_input(input: str) -> list[str]:
    f = open(input, "r")
    grid = f.read().split("\n")
    f.close()
    return grid


def get_start(grid: list[str]) -> (int, int):
    for y in range(len(grid)):
        x = grid[y].find("S")
        if x != -1:
            return (x, y)


# https://github.com/CalSimmon/advent-of-code/blob/main/2023/day_21/solution.py
# Part 1
# BFS to get number of tiles for any given distance from the starting point
def possible_titles(
    tile: tuple[int, int], grid: list[str]
) -> Generator[tuple[int, int]]:
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    for direction in directions:
        new_point = (tile[0] + direction[0], tile[1] + direction[1])
        if grid[new_point[1] % len(grid)][new_point[0] % len(grid)] != "#":
            yield new_point


def get_possible_tiles(
    grid: list[str], start: tuple[int, int], steps: int
) -> dict[int, int]:
    tiles = defaultdict(int)
    visited = set()
    to_visit = [(start, 0)]
    while to_visit:
        current_tile, distance = to_visit.pop(0)
        if distance == steps + 1 or current_tile in visited:
            continue
        tiles[distance] += 1
        visited.add(current_tile)

        for next_tile in possible_titles(current_tile, grid):
            to_visit.append((next_tile, distance + 1))
    return tiles


def calculate_possible_tiles(
    grid: list[str], start: tuple[int, int], steps: int
) -> int:
    distance_to_tiles = get_possible_tiles(grid, start, steps)
    return sum(
        num_tiles
        for distance, num_tiles in distance_to_tiles.items()
        # Because you can step back and forth onto tiles in subsequent steps, only
        # sum every other tile based on the number of steps
        # (i.e. only the odds for an odd number of steps etc.)
        if (distance % 2 == steps % 2)
    )


# Part 2
# For this one, you can't brute force it.
# Number of possible tiles is a quadratic
# Can use 1st 3 points to determine an equation
# In this case, the fit for small numbers is slightly off for big numbers
# and vice versa.
# So use datapoints f(S), f(S + X), f(S + 2*X)
#   - S = starting point = len(grid)/2
#   - X = grid size = len(grid)
def get_quadratic(points: list[int]) -> Callable:
    a = (points[2] - (2 * points[1]) + points[0]) // 2
    b = points[1] - points[0] - a
    c = points[0]

    return lambda x: (a * x**2) + (b * x) + c


def get_infinite_grid_tiles(grid: list[str], start: tuple[int, int], goal: int) -> int:
    X = len(grid)
    S = X // 2

    points = [calculate_possible_tiles(grid, start, S + (i * X)) for i in range(3)]
    quad = get_quadratic(points)
    return quad(((goal - S) // X))


if __name__ == "__main__":
    grid = handle_input("puzzle input.txt")
    start = get_start(grid)
    print(f"Part 1: {calculate_possible_tiles(grid, start, 64)}")
    print(f"Part 2: {get_infinite_grid_tiles(grid, start, 26501365)}")
