#!/usr/bin/env python3

# Based off of https://scalacenter.github.io/scala-advent-of-code/2023/puzzles/day03
import re
from typing import TextIO
from collections.abc import Iterable, Callable


class Coordinate:
    def __init__(self, x: str, y: str):
        self.x = x
        self.y = y

    def within(self, start: "Coordinate", end: "Coordinate") -> bool:
        if self.y < start.y or self.y > end.y:
            return False
        elif self.x < start.x or self.x > end.x:
            return False
        else:
            return True


class PartNumber:
    def __init__(self, value: int, start: Coordinate, end: Coordinate):
        self.value = value
        self.start = start
        self.end = end


class Symbol:
    def __init__(self, value: str, position: Coordinate):
        self.value = value
        self.position = position

    def neighbor_of(self, part: PartNumber) -> bool:
        return self.position.within(
            Coordinate(part.start.x - 1, part.start.y - 1),
            Coordinate(part.end.x + 1, part.end.y + 1),
        )


def match_is_int(match: re.Match) -> bool:
    try:
        int(match.group(0))
        return True
    except:
        return False


def flat_map(
    f: Callable[[tuple, str], list], xs: Iterable[tuple[int, tuple[str]]], *argv
) -> list:
    ys = []
    for x in xs:
        ys.extend(f(x, argv[0]))
    return ys


def categorize_parts_and_symbols(x: tuple[int, tuple[str]], extractor: str) -> list:
    i, line = x
    line = line[0]
    return [
        PartNumber(
            int(match.group(0)),
            Coordinate(match.start(), i),
            Coordinate(match.end() - 1, i),
        )
        if match_is_int(match)
        else Symbol(match.group(0), Coordinate(match.start(), i))
        for match in re.finditer(extractor, line)
    ]


def find_parts_and_symbols(source: TextIO) -> list:
    extractor = r"(\d+)|[^.]"
    return flat_map(
        categorize_parts_and_symbols,
        enumerate(zip(source.read().split("\n"))),
        extractor,
    )


def sum_part_numbers(input: str) -> int:
    f = open(input, "r")

    # All symbols and numbers (non-periods)
    all = find_parts_and_symbols(f)

    # lesson learned: a filter returns a filter object and can't be used for comparison, need to unpack to a list
    symbols = [symbol for symbol in filter(lambda x: type(x) == Symbol, all)]

    parts = [
        part
        for part in filter(
            lambda y: type(y) == PartNumber
            and any(symbol.neighbor_of(y) for symbol in symbols),
            all,
        )
    ]

    numbers = [part.value for part in parts]
    f.close()
    return sum(numbers)


if __name__ == "__main__":
    print(sum_part_numbers("./puzzle input.txt"))
