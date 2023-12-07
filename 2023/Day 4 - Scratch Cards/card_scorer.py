#!/usr/bin/env python3
import re


class Card:
    def __init__(self, line: str):
        label, numbers = line.split(": ")
        win, owned = numbers.split(" | ")
        self.number = int(re.search(r"\d+", label).group())
        self.winning_numbers = [int(n) for n in re.findall(r"\d+", win)]
        self.owned_numbers = [int(n) for n in re.findall(r"\d+", owned)]
        self.matches = [n for n in self.owned_numbers if n in self.winning_numbers]
        self.score = len(self.matches)
        # part 1
        if self.score:
            self.points = 2 ** (self.score - 1)
        else:
            self.points = self.score


def get_card_points(source: str) -> int:
    f = open(source, "r")
    lines = f.read().split("\n")

    cards = [Card(line) for line in lines]
    scores = [card.points for card in cards]

    f.close()
    return sum(scores)


if __name__ == "__main__":
    print("Part 1:", get_card_points("./puzzle input.txt"))
