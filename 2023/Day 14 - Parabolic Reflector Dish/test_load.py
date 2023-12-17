#!/usr/bin/env python3
import re


def handle_input(input: str) -> list[str]:
    f = open(input, "r")
    rows = f.read().split("\n")
    f.close()
    return rows


def move_north(rows: list[str]) -> list[list[str]]:
    columns = list(zip(*rows))
    sorted_columns = []
    for column in columns:
        segments = [list(segment) for segment in "".join(column).split("#")]
        for segment in segments:
            segment.sort(reverse=True)
        sorted_column = []
        for i in range(len(segments)):
            if segments[i]:
                sorted_column.extend(segments[i])
                # Make sure that we don't add an extra "#" at the end of the column
                if i < len(segments) - 1:
                    sorted_column.append("#")
            else:
                if i < len(segments) - 1:
                    # Because of using split(), empty lists represent "#" characters
                    sorted_column.append("#")
        sorted_columns.append(sorted_column)
    return sorted_columns


def calculate_load(sorted_columns: list[list[str]]) -> int:
    pattern = r"[O]"
    load = 0
    for column in sorted_columns:
        # reverse it because "O"s at the "top" is has most load
        for match in re.finditer(pattern, "".join(reversed(column))):
            load += match.start() + 1
    return load


if __name__ == "__main__":
    rows = handle_input("puzzle input.txt")
    print(f"Part 1: {calculate_load(move_north(rows))}")
