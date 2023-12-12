#!/usr/bin/env python3


def get_readings(input: str) -> list[list[int]]:
    f = open(input, "r")
    numbers = [
        [int(entry) for entry in data.split(" ")] for data in f.read().split("\n")
    ]
    return numbers


# Part 1
def calculate_prediction(readings: list[int]) -> int:
    if len(readings) == 0:
        return 0
    differences = [readings[i + 1] - readings[i] for i in range(len(readings) - 1)]
    return readings[-1] + calculate_prediction(differences)


def get_all_predictions(input: str) -> int:
    all_readings = get_readings(input)
    predictions = [calculate_prediction(readings) for readings in all_readings]
    return sum(predictions)


# Part 2
def calculate_extrapolation(readings: list[int]) -> int:
    if len(readings) == 0:
        return 0
    differences = [readings[i + 1] - readings[i] for i in range(len(readings) - 1)]
    return readings[0] - calculate_extrapolation(differences)


def get_all_extrapolations(input: str) -> int:
    all_readings = get_readings(input)
    extrapolations = [calculate_extrapolation(readings) for readings in all_readings]
    return sum(extrapolations)


if __name__ == "__main__":
    print(f"Part 1: {get_all_predictions('puzzle input.txt')}")
    print(f"Part 2: {get_all_extrapolations('puzzle input.txt')}")
