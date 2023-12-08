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
        self.copies = 1


# Part 1
def get_card_points(source: str) -> int:
    f = open(source, "r")
    lines = f.read().split("\n")

    cards = [Card(line) for line in lines]
    scores = [card.points for card in cards]

    f.close()
    return sum(scores)


# Part 2
def get_card_copies(source: str) -> int:
    f = open(source, "r")
    lines = f.read().split("\n")

    cards = [Card(line) for line in lines]

    for i in range(len(cards)):
        if cards[i].score > 0:
            for j in range(1, cards[i].score + 1):
                cards[i + j].copies += cards[i].copies

    copies = [card.copies for card in cards]
    return sum(copies)


if __name__ == "__main__":
    print("Part 1:", get_card_points("./puzzle input.txt"))
    print("Part 2:", get_card_copies("./puzzle input.txt"))
