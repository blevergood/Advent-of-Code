#!/usr/bin/env python3
import re


def get_card_points(source: str) -> int:
    scores = []

    f = open(source, "r")
    lines = f.read().split("\n")

    for line in lines:
        numbers = line.split(": ")[1]
        winning_numbers_s, card_numbers_s = numbers.split(" | ")

        winning_numbers_n = [int(n) for n in re.findall(r"\d+", winning_numbers_s)]
        card_numbers_n = [int(n) for n in re.findall(r"\d+", card_numbers_s)]

        # Assuming that we could have repeated numbers in either list, so Set Intersection won't work
        matches = [n for n in card_numbers_n if n in winning_numbers_n]
        if len(matches):
            scores.append(2 ** (len(matches) - 1))
        else:
            # superfluous but makes it comprehensive & explicit
            scores.append(0)

    f.close()
    return sum(scores)


if __name__ == "__main__":
    print("Part 1:", get_card_points("./puzzle input.txt"))
