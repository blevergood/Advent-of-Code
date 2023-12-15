#!/usr/bin/env python3
import re
import sys
from collections.abc import Callable
from bidict import bidict


class AlmanacRange:
    def __init__(self, start: int, length: int) -> None:
        self.start = start
        self.end = start + length - 1

    def contains(self, value: int) -> bool:
        if value < self.start:
            return False
        elif value > self.end:
            return False
        else:
            return True

    def get_bounds(self) -> list[int]:
        return [self.start - 1, self.start, self.end, self.end + 1]

    def expand(self) -> list[int]:
        return list(range(self.start, self.end + 1))


class AlmanacMap:
    def __init__(self, ranges: list[list[int]]) -> None:
        self.mapping = bidict()
        for r in ranges:
            dest_start, src_start, length = r
            self.mapping[AlmanacRange(src_start, length)] = AlmanacRange(
                dest_start, length
            )

    def get_inverse(self):
        return self.mapping

    def mapped_number(self, src: int) -> int:
        for k in self.mapping.keys():
            if k.contains(src):
                return self.mapping[k].start + (src - k.start)
        return src

    def inverted_number(self, dest: int) -> int:
        for k in self.mapping.inverse.keys():
            if k.contains(dest):
                return self.mapping.inverse[k].start + (dest - k.start)
        return dest


def get_maps(segments: list[str]) -> list[AlmanacMap]:
    return [
        AlmanacMap(
            [
                [int(match) for match in re.findall(r"\d+", map)]
                for map in segment.split("\n")[1:]
            ]
        )
        for segment in segments
    ]


# Part 1
def get_seeds_list(line: str) -> list[int]:
    return [int(match) for match in re.findall(r"\d+", line)]


# Part 2
def get_seeds_ranges(line: str) -> list[AlmanacRange]:
    numbers = get_seeds_list(line)
    return [AlmanacRange(*numbers[i : i + 2]) for i in range(0, len(numbers), 2)]


def get_seeds_to_check(line: str, maps=list[AlmanacMap]) -> list[int]:
    """
    The challenge here is that it takes too long to manually process all available seeds
    We only need to check the bounds of seeds corresponding to each map's piecewise equations
    Concept from:
    https://www.reddit.com/r/adventofcode/comments/18b4b0r/comment/kc3q9c6/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    """
    seed_ranges = get_seeds_ranges(line)

    # Bounds of locations is entire range
    potential_seeds = [0, sys.maxsize]

    # Figure out bounds by walking backwards through mapping
    for map in reversed(maps):
        # Only iterate over seeds of the previous layers (don't double-translate new values)
        current_seeds = len(potential_seeds)
        # Translation of each previous layer boundary to current-layer values
        for i in range(current_seeds):
            potential_seeds.append(map.inverted_number(potential_seeds[i]))
        # Add current-layer boundaries
        for r in map.mapping.keys():
            potential_seeds.extend(r.get_bounds())
        # Eliminate any duplicates
        potential_seeds = list(set(potential_seeds))

    seeds_to_check = []

    # Intersection between bounds-based potential seeds and available seeds in the ranges
    for r in seed_ranges:
        for seed in potential_seeds:
            if r.contains(seed):
                seeds_to_check.append(seed)

    return seeds_to_check


def get_closest_location(source: str, func: Callable[[str], list[int]]) -> int:
    f = open(source, "r")
    segments = f.read().split("\n\n")
    f.close()

    arguments = [segments.pop(0)]
    maps = get_maps(segments)

    if func == get_seeds_to_check:
        arguments.append(maps)

    seeds = func(*arguments)

    (
        seed_soil,
        soil_fertilizer,
        fertilizer_water,
        water_light,
        light_temp,
        temp_humid,
        humid_location,
    ) = maps

    locations = [
        humid_location.mapped_number(
            temp_humid.mapped_number(
                light_temp.mapped_number(
                    water_light.mapped_number(
                        fertilizer_water.mapped_number(
                            soil_fertilizer.mapped_number(seed_soil.mapped_number(seed))
                        )
                    )
                )
            )
        )
        for seed in seeds
    ]

    return min(locations)


if __name__ == "__main__":
    print(f"Part 1: {get_closest_location('./puzzle input.txt', get_seeds_list)}")
    print(f"Part 2: {get_closest_location('./puzzle input.txt', get_seeds_to_check)}")