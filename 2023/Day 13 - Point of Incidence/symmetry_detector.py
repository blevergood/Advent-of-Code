#!/usr/bin/env python3

# Solution from: https://advent-of-code.xavd.id/writeups/2023/day/13/
# Had trouble conceptualizing symmetry in a list of strings.


# Used different variable names and added to help myself cement understanding of why this works.
def handle_input(input: str) -> list[list[str]]:
    f = open(input, "r")
    segments = [segment.split("\n") for segment in f.read().split("\n\n")]
    f.close()
    return segments


# You need to find the substring with exactly one difference
# This function will return 0 for symmetrical strings and large numbers
# For non-symmetrical strings, but exactly 1 for the string with the "smudge"
def str_differences(left: str, right: str) -> int:
    # Booleans are counted as 0/1 and can be summed together
    return sum(a != b for a, b in zip(left, right))


# For each index, check substring equality along that "line"
# Plug in the original list as well as a rotated copy of the list
# to check both dimensions of symmetry
def reflection(segment: list[str], num_smudges: int) -> int:
    # 0 can't be the reflection index
    for index in range(1, len(segment)):
        if (
            sum(
                str_differences(left, right)
                for left, right in zip(reversed(segment[:index]), segment[index:])
            )
            == num_smudges
        ):
            return index
    return 0


def get_score(segment: list[str], num_smudges: int) -> int:
    if row := reflection(segment, num_smudges):
        return 100 * row
    # list(zip()) rotates the contents if each string is the same length (which is guaranteed in this case).
    # Also see og solution for 2023/Day 11 - Cosmic Expanse
    if col := reflection(list(zip(*segment)), num_smudges):
        return col


if __name__ == "__main__":
    segments = handle_input("puzzle input.txt")
    scores = [get_score(segment, 0) for segment in segments]
    print(f"Part 1: {sum(scores)}")
    smudge_scores = [get_score(segment, 1) for segment in segments]
    print(f"Part 2: {sum(smudge_scores)}")
