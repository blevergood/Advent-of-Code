#!/usr/bin/env python3
def minimum_cubes_power(input):
    f = open(input, "r")
    powers = [game_power(game) for game in f.readlines()]
    f.close()
    return sum(powers)


def game_power(game):
    rounds_t = game.split(": ")[1]
    rounds = [get_round_map(round) for round in rounds_t.split("; ")]
    game_minimums = get_game_minimums(rounds)
    power = 1
    for key in game_minimums.keys():
        power *= game_minimums[key]
    return power


def get_round_map(round):
    cubes = round.split(", ")
    round_map = {}
    for cube in cubes:
        v, k = cube.split(" ")
        round_map[k.strip()] = int(v)
    return round_map


def get_game_minimums(rounds):
    game_minimums = {"red": 0, "green": 0, "blue": 0}
    for round in rounds:
        for key in game_minimums.keys():
            if round.get(key, 0) > game_minimums.get(key, 0):
                game_minimums[key] = round.get(key, 0)
    return game_minimums


if __name__ == "__main__":
    print(minimum_cubes_power("./puzzle input.txt"))
