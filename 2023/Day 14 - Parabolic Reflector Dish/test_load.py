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


# Part 1
def calculate_load(sorted_grid: str) -> int:
    pattern = r"[O]"
    load = 0
    sorted_columns = list(zip(*sorted_grid.split("\n")))
    for column in sorted_columns:
        # reverse it because "O"s at the "top" is has most load
        for match in re.finditer(pattern, "".join(reversed(column))):
            load += match.start() + 1
    return load


# Part 2
# Need to get more familiar with caching/dynamic programming approaches
# https://topaz.github.io/paste/#XQAAAQCfBQAAAAAAAAA0m0pnuFI8c914retSmoIG37eNoSYboE7/gbzaWCjBIXsYaqs/ZhF4zXxknPskUKlzaTugMLJ86BL48Z/bBaecxEslMxPaolHPUZdPFtiK5unUUlCJBQY25PvpGJRn4dJoIn/9SVca9QEGd1lsW+1BHHj7QumTbXdEIJdYBynB4MJvhDcQMb0CRgbL1xIkJ3H+CPIT6aJQYYusYtC8JWQhYn6N/MBHhPP2q4rIoEIsG3XH2G0SiG+j/zTxW7FTBZk+LBZGe+x1OXHAIfUt1JL8au+YGF2xp9Fmehenq9E4lVh0xGmGD72ODU08kg8LsWK39qZAaUgTydehQ9yUP79INCqrVWxq/yWYlUbqH9crAv/uWAsubVOLz2S0K9qrsGBnTqDU8prITvNAfml4e6kegqAUozLYidAmK1Nsj0EPSKio2SmmPtZqFqbOvCkHhJ+e8mqTBDJrZ3r+UYrjrSgpDaXJ8q3nmgIeZb/VFlnf2dtPZTHdR1G1lTRPG8ArNHkGfh+GDUPJM7Q7Cz8rO6prNn5l5Wcyk3Y0KpuzRndSD6N22mz1l9lN5uq3tgu+1CikaHNzJPnkLMLrNfeBX9eeZkJNdE12mtVFAoqvcNcNfUO/rZCJkUjaErUjYm5hkfMWm4zvsO0YsDClvWvsggN0x5Tx37TDER940a1xpHnnBDkeKXw7wOiFMun8GGh5dsqO1jI0oEU7FGiizidCOP2ruFd9he2Tyfdidpm8yWtztNmm9f297xyyrIctBcMi7wWBoT7o0mvGBe3KD/7azdqFRuNj1w0clQSAKxvFUgdJG3pN//fAQ+A=
def calculate_many_rotations_load(grid: str, rotations: int) -> int:
    rot_cache = {}
    rotation = 0
    found_pattern = False
    while rotation < rotations:
        for direction in ["north", "west", "south", "east"]:
            grid = move(grid, direction)
        rotation += 1

        if not found_pattern and (found_pattern := grid in rot_cache):
            pattern_length = rotation - rot_cache[grid]
            rotation += pattern_length * ((rotations - rotation) // pattern_length)
        else:
            rot_cache[grid] = rotation
    return calculate_load(grid)


if __name__ == "__main__":
    grid = handle_input("puzzle input.txt")
    print(f"Part 1: {calculate_load(move(grid, 'north'))}")
    print(f"Part 2: {calculate_many_rotations_load(grid, 1000000000)}")
