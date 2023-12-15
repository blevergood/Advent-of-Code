#!/usr/bin/env python3
import re


def get_universe(input: str) -> list[str]:
    f = open(input, "r")
    all = f.read()
    lines = all.split("\n")
    f.close()
    return lines


def expand_universe(universe: list[str]) -> list[str]:
    empty_rows = [i for i in range(len(universe)) if "#" not in universe[i]]
    for i in range(len(empty_rows)):
        universe.insert(empty_rows[i] + i, universe[empty_rows[i] + i])
    universe_transpose = ["".join(column) for column in zip(*universe)]
    empty_columns = [
        i for i in range(len(universe_transpose)) if "#" not in universe_transpose[i]
    ]
    for i in range(len(empty_columns)):
        universe_transpose.insert(empty_columns[i] + i, universe_transpose[empty_columns[i] + i])

    return ["".join(row) for row in zip(*universe_transpose)]



def get_galaxies(universe: list[str]) -> list[(int, int)]:
    expression = r"[#]"
    return [
        (m.start(), i)
        for i in range(len(universe))
        for m in re.finditer(expression, universe[i])
    ]


def calculate_distances(galaxies: list[(int, int)]) -> list[int]:
    distances = []
    while len(galaxies) > 0:
        current = galaxies.pop()
        distances.extend(
            [
                abs(current[0] - other[0]) + abs(current[1] - other[1])
                for other in galaxies
            ]
        )
    return distances


if __name__ == "__main__":
    og_universe = get_universe("./puzzle input.txt")
    universe = expand_universe(og_universe)
    distances = calculate_distances(get_galaxies(universe))
    print(f"Part 1: {sum(distances)}")
