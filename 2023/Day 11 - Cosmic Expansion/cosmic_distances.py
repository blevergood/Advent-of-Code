#!/usr/bin/env python3
import re


def get_universe(input: str) -> list[str]:
    f = open(input, "r")
    all = f.read()
    lines = all.split("\n")
    f.close()
    return lines


# This was the main function that changed between Part 1 & Part 2
# Went from inserting a few strings into the text
# to multiplying by the number of empty strings
def expand_universe(universe: list[str]) -> (list[int], list[int]):
    empty_rows = [i for i in range(len(universe)) if "#" not in universe[i]]
    universe_transpose = ["".join(column) for column in zip(*universe)]
    empty_columns = [
        i for i in range(len(universe_transpose)) if "#" not in universe_transpose[i]
    ]

    return (empty_columns, empty_rows)


def is_between(coord: int, a: int, b: int) -> bool:
    return (a > coord and b < coord) or (b > coord and a < coord)


def get_galaxies(universe: list[str]) -> list[(int, int)]:
    expression = r"[#]"
    return [
        (m.start(), i)
        for i in range(len(universe))
        for m in re.finditer(expression, universe[i])
    ]


def calculate_distances(
    galaxies: list[(int, int)], coords_x, coords_y, expand_factor
) -> list[int]:
    distances = []
    while len(galaxies) > 0:
        current = galaxies.pop()
        for other in galaxies:
            distance = abs(current[0] - other[0]) + abs(current[1] - other[1])
            for x in coords_x:
                if is_between(x, current[0], other[0]):
                    distance += expand_factor - 1
            for y in coords_y:
                if is_between(y, current[1], other[1]):
                    distance += expand_factor - 1
            distances.append(distance)
    return distances


if __name__ == "__main__":
    universe = get_universe("./puzzle input.txt")
    coords_x, coords_y = expand_universe(universe)
    distances = calculate_distances(get_galaxies(universe), coords_x, coords_y, 2)
    print(f"Part 1: {sum(distances)}")

    distances_2 = calculate_distances(
        get_galaxies(universe), coords_x, coords_y, int(1e6)
    )
    print(f"Part 2: {sum(distances_2)}")
