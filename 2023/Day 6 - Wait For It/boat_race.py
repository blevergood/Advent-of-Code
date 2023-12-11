#!/usr/bin/env python3
import re
import math
from functools import reduce


class BoatRace:
    def __init__(self, time, distance) -> None:
        self.time = time
        self.distance = distance

    def button_press_boundaries(self) -> list[int]:
        # Get roots of quadratic equation:
        # self.distance = hold_time * (self.time - hold_time)
        # = self.distance = -hold_time**2 + hold_time * self.time
        return [
            -1 * (-1 * self.time + math.sqrt(self.time**2 - 4 * self.distance)) / 2,
            -1 * (-1 * self.time - math.sqrt(self.time**2 - 4 * self.distance)) / 2,
        ]

    def possible_wins(self) -> int:
        minimum, maximum = self.button_press_boundaries()
        if maximum % 1 == 0:
            maximum -= 1
        return int(maximum) - int(minimum)


# Part 1
def get_total_multi_margin(input: str) -> int:
    f = open(input, "r")

    times, distances = [
        [int(n) for n in re.findall(r"\d+", line)] for line in f.read().split("\n")
    ]

    f.close()

    races = [BoatRace(x, y) for x, y in zip(times, distances)]
    num_wins = [race.possible_wins() for race in races]
    return reduce((lambda x, y: x * y), num_wins)


# Part 2
def get_single_margin(input: str) -> int:
    f = open(input, "r")
    time, distance = [
        int("".join(re.findall(r"\d+", line))) for line in f.read().split("\n")
    ]
    f.close()

    race = BoatRace(time, distance)
    return race.possible_wins()


if __name__ == "__main__":
    print("Part 1:", get_total_multi_margin("./puzzle input.txt"))
    print("Part 2:", get_single_margin("./puzzle input.txt"))
