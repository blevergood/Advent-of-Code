#!/usr/bin/env python3
import re


def handle_input(input: str) -> list[str]:
    f = open(input, "r")
    grid = f.read()
    f.close()
    return grid


def move(grid: str, direction: str) -> str:
    # column sorting
    rows = grid.split("\n")
    if direction in ["north", "south"]:
        arrays = list(zip(*rows))
        reversed = direction == "north"
    else:
        arrays = [tuple(row) for row in rows]
        reversed = direction == "west"
    sorted_arrays = []
    for array in arrays:
        segments = [list(segment) for segment in "".join(array).split("#")]
        for segment in segments:
            segment.sort(reverse=reversed)
        sorted_array = []
        for i in range(len(segments)):
            if segments[i]:
                sorted_array.extend(segments[i])
                # Make sure that we don't add an extra "#" at the end of the column
            if i < len(segments) - 1:
                sorted_array.append("#")
        sorted_arrays.append(sorted_array)
    # Maintain string stucture
    if direction in ["north", "south"]:
        sorted_grid = "\n".join(["".join(array) for array in (zip(*sorted_arrays))])
    else:
        sorted_grid = "\n".join(["".join(array) for array in sorted_arrays])
    return sorted_grid


def calculate_load(sorted_grid: str) -> int:
    pattern = r"[O]"
    load = 0
    sorted_columns = list(zip(*sorted_grid.split("\n")))
    for column in sorted_columns:
        # reverse it because "O"s at the "top" is has most load
        for match in re.finditer(pattern, "".join(reversed(column))):
            load += match.start() + 1
    return load


if __name__ == "__main__":
    grid = handle_input("example.txt")
    print(f"Part 1: {calculate_load(move(grid, 'north'))}")
