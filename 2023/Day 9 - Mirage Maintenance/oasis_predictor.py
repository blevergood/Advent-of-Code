#!/usr/bin/env python3
def get_readings(input: str) -> list[list[int]]:
    f = open(input, "r")
    numbers = [
        [int(entry) for entry in data.split(" ")] for data in f.read().split("\n")
    ]
    return numbers


def calculate_extrapolation(readings: list[int], backward=False) -> int:
    if len(readings) == 0:
        return 0
    # Part 2
    if backward:
        func = lambda x, y: x - y
        target_int = 0
    # Part 1
    else:
        func = lambda x, y: x + y
        target_int = -1
    differences = [readings[i + 1] - readings[i] for i in range(len(readings) - 1)]
    return func(readings[target_int], calculate_extrapolation(differences, backward))


def get_all_extrapolations(input: str, backward=False) -> int:
    all_readings = get_readings(input)
    extrapolations = [
        calculate_extrapolation(readings, backward) for readings in all_readings
    ]
    return sum(extrapolations)


if __name__ == "__main__":
    print(f"Part 1: {get_all_extrapolations('puzzle input.txt')}")
    print(f"Part 2: {get_all_extrapolations('puzzle input.txt', backward=True)}")
