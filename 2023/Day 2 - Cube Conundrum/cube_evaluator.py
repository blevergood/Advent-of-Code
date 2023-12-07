#!/usr/bin/env python3
from part_1_games_validator import validate_games
from part_2_minimum_cubes import minimum_cubes_power


if __name__ == "__main__":
    print("Part 1:", validate_games("./puzzle input.txt"))
    print("Part 2", minimum_cubes_power("./puzzle input.txt"))
