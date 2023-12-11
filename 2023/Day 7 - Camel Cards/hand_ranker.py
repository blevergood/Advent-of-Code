#!/usr/bin/env python3
from itertools import groupby


class Card:
    def __init__(self, label: str) -> None:
        self.label = label

    def __str__(self) -> str:
        return self.label

    def __eq__(self, other: "Card") -> bool:
        if isinstance(other, Card):
            return self.label == other.label
        return False

    def __lt__(self, other: "Card") -> bool:
        if isinstance(other, Card):
            # Part 2
            if isinstance(self, WildCard) or isinstance(other, WildCard):
                values = [
                    "J",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "T",
                    "Q",
                    "K",
                    "A",
                ]
            # Part 1
            else:
                values = [
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "T",
                    "J",
                    "Q",
                    "K",
                    "A",
                ]
            return values.index(self.label) < values.index(other.label)
        return NotImplemented

    def __le__(self, other: "Card") -> bool:
        if isinstance(other, Card):
            if isinstance(self, WildCard) or isinstance(other, WildCard):
                values = [
                    "J",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "T",
                    "Q",
                    "K",
                    "A",
                ]
            else:
                values = [
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "T",
                    "J",
                    "Q",
                    "K",
                    "A",
                ]
            return values.index(self.label) <= values.index(other.label)
        return NotImplemented

    def _gt_(self, other: "Card") -> bool:
        if isinstance(other, Card):
            if isinstance(self, WildCard) or isinstance(other, WildCard):
                values = [
                    "J",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "T",
                    "Q",
                    "K",
                    "A",
                ]
            else:
                values = [
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "T",
                    "J",
                    "Q",
                    "K",
                    "A",
                ]
            return values.index(self.label) > values.index(other.label)
        return NotImplemented

    def _ge_(self, other: "Card") -> bool:
        if isinstance(other, Card):
            if isinstance(self, WildCard) or isinstance(other, WildCard):
                values = [
                    "J",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "T",
                    "Q",
                    "K",
                    "A",
                ]
            else:
                values = [
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "T",
                    "J",
                    "Q",
                    "K",
                    "A",
                ]
            return values.index(self.label) >= values.index(other.label)
        return NotImplemented


# Part 2
class WildCard(Card):
    def __init__(self, label: str) -> None:
        super(WildCard, self).__init__(label)


class Hand:
    def __init__(self, cards: list[Card | WildCard]) -> None:
        self.cards = cards
        self._current_index = 0
        if any([isinstance(card, Card) for card in cards]):
            cards = self.transform_wildcards()
        groups = [list(g) for k, g in groupby((sorted(cards)))]
        # Four of a kind OR Full House
        if len(groups) == 1:
            self.type = "FIVE"
        elif len(groups) == 2:
            if len(groups[0]) == 4 or len(groups[1]) == 4:
                self.type = "FOUR"
            else:
                self.type = "FULL"
        elif len(groups) == 3:
            if len(groups[0]) == 3 or len(groups[1]) == 3 or len(groups[2]) == 3:
                self.type = "THREE"
            else:
                self.type = "TWOPAIR"
        elif len(groups) == 4:
            self.type = "PAIR"
        else:
            self.type = "HIGHCARD"

    def __str__(self) -> str:
        return "".join(str(card) for card in self.cards)

    def __eq_(self, other: "Hand") -> bool:
        return self.cards == other.cards

    def __lt__(self, other: "Hand") -> bool:
        types = ["HIGHCARD", "PAIR", "TWOPAIR", "THREE", "FULL", "FOUR", "FIVE"]
        if isinstance(other, Hand):
            if self.type != other.type:
                return types.index(self.type) < types.index(other.type)
            else:
                for i in range(len(self.cards)):
                    if self.cards[i] != other.cards[i]:
                        return self.cards[i] < other.cards[i]
                return False
        return NotImplemented

    def __le__(self, other: "Hand") -> bool:
        types = ["HIGHCARD", "PAIR", "TWOPAIR", "THREE", "FULL", "FOUR", "FIVE"]
        if isinstance(other, Hand):
            if self.type != other.type:
                return types.index(self.type) <= types.index(other.type)
            else:
                for i in range(len(self.cards)):
                    if self.cards[i] != other.cards[i]:
                        return self.cards[i] <= other.cards[i]
                return False
        return NotImplemented

    def __gt__(self, other: "Hand") -> bool:
        types = ["HIGHCARD", "PAIR", "TWOPAIR", "THREE", "FULL", "FOUR", "FIVE"]
        if isinstance(other, Hand):
            if self.type != other.type:
                return types.index(self.type) > types.index(other.type)
            else:
                for i in range(len(self.cards)):
                    if self.cards[i] != other.cards[i]:
                        return self.cards[i] > other.cards[i]
                return False
        return NotImplemented

    def __ge__(self, other: "Hand") -> bool:
        types = ["HIGHCARD", "PAIR", "TWOPAIR", "THREE", "FULL", "FOUR", "FIVE"]
        if isinstance(other, Hand):
            if self.type != other.type:
                return types.index(self.type) >= types.index(other.type)
            else:
                for i in range(len(self.cards)):
                    if self.cards[i] != other.cards[i]:
                        return self.cards[i] >= other.cards[i]
                return False
        return NotImplemented

    # Part 2
    def transform_wildcards(self) -> list[Card|WildCard]:
        normal_cards = [card for card in self.cards if not isinstance(card, WildCard)]
        wild_cards = [card for card in self.cards if isinstance(card, WildCard)]
        if normal_cards:
            mode_card = max(normal_cards, key=normal_cards.count)
            for card in wild_cards:
                normal_cards.append(mode_card)
            return normal_cards
        else:
            return wild_cards


# Part 1
def get_total_winnings_normal(input: str) -> int:
    f = open(input, "r")
    table = {}
    for line in f.read().split("\n"):
        values, bet = line.split(" ")
        table[Hand([Card(value) for value in values])] = int(bet)
    sorted_hands = sorted([key for key in table.keys()])

    winnings = [(i + 1) * table[sorted_hands[i]] for i in range(len(sorted_hands))]
    return sum(winnings)


# Part 2
def get_total_winnings_wild(input: str) -> int:
    f = open(input, "r")
    table = {}
    for line in f.read().split("\n"):
        values, bet = line.split(" ")
        table[
            Hand([Card(value) if value != "J" else WildCard(value) for value in values])
        ] = int(bet)
    sorted_hands = sorted([key for key in table.keys()])

    winnings = [(i + 1) * table[sorted_hands[i]] for i in range(len(sorted_hands))]
    return sum(winnings)


if __name__ == "__main__":
    print(f"Part 1: {get_total_winnings_normal('puzzle input.txt')}")
    print(f"Part 2: {get_total_winnings_wild('puzzle input.txt')}")
