#!/usr/bin/env python3
def handle_input(input: str) -> list[list[str]]:
    f = open(input, "r")
    segments = [segment.split("\n") for segment in f.read().split("\n\n")]
    f.close()
    return segments


def reflection(segment: list[str]) -> int:
    # 0 can't be the reflection index
    for index in range(1, len(segment)):
        if all(
            left == right
            for left, right in zip(reversed(segment[:index]), segment[index:])
        ):
            return index
    return 0


def get_score(segment: list[str]) -> int:
    if row := reflection(segment):
        return 100 * row
    if col := reflection(list(zip(*segment))):
        return col

if __name__ == '__main__':
    segments = handle_input("puzzle input.txt")
    scores = [get_score(segment) for segment in segments]
    print(f"Part 1: {sum(scores)}")