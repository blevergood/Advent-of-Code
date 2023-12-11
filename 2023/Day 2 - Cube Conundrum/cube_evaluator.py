#!/usr/bin/env python3
def get_round_map(round: str) -> dict[str, int]:
    cubes = round.split(", ")
    round_map = {}
    for cube in cubes:
        v, k = cube.split(" ")
        round_map[k.strip()] = int(v)
    return round_map


# Part 1
def validate_round(
    round: str, limits: dict[str, int] = {"red": 12, "green": 13, "blue": 14}
) -> bool:
    for key in round.keys():
        if round[key] > limits[key]:
            return False
    return True


def validate_game(game: str) -> int:
    game_t, rounds_t = game.split(": ")
    game_n = int(game_t.split(" ")[1])
    rounds = [get_round_map(round) for round in rounds_t.split("; ")]
    rounds_valid = [validate_round(round) for round in rounds]
    if False in rounds_valid:
        return 0
    return game_n


def validate_games(input: str) -> int:
    f = open(input, "r")
    games = [validate_game(game) for game in f.readlines()]
    f.close()
    return sum(games)


# Part 2
def get_game_minimums(rounds: list[dict[str, int]]) -> dict[str, int]:
    game_minimums = {"red": 0, "green": 0, "blue": 0}
    for round in rounds:
        for key in game_minimums.keys():
            if round.get(key, 0) > game_minimums.get(key, 0):
                game_minimums[key] = round.get(key, 0)
    return game_minimums


def game_power(game: str) -> int:
    rounds_t = game.split(": ")[1]
    rounds = [get_round_map(round) for round in rounds_t.split("; ")]
    game_minimums = get_game_minimums(rounds)
    power = 1
    for key in game_minimums.keys():
        power *= game_minimums[key]
    return power


def minimum_cubes_power(input: str) -> int:
    f = open(input, "r")
    powers = [game_power(game) for game in f.readlines()]
    f.close()
    return sum(powers)


if __name__ == "__main__":
    print(f"Part 1: {validate_games('./puzzle input.txt')}")
    print(f"Part 2: {minimum_cubes_power('./puzzle input.txt')}")