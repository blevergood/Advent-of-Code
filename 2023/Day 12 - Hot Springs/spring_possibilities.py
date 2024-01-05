#!/usr/bin/env python3
import re
from itertools import combinations
from functools import cache


def process_input(input: str) -> (list[str], list[int]):
    f = open(input, "r")
    lines = f.read().split("\n")
    f.close()

    rows, sequences = [], []
    for line in lines:
        row, seq_str = line.split(" ")
        seq = [int(n) for n in seq_str.split(",")]
        rows.append(row)
        sequences.append(tuple(seq))
    return rows, tuple(sequences)


# Part 1 - Brute Force
def get_index_permutations(rows: list[list[str]]) -> list[list[tuple[int]]]:
    expression = r"[\?]"
    question_marks = [[m.start() for m in re.finditer(expression, row)] for row in rows]
    index_permutations = []
    for row in question_marks:
        current_perms = []
        for i in range(len(row) + 1):
            current_perms.extend(list(combinations(row, i)))
        index_permutations.append(current_perms)
    return index_permutations


def get_possible_strings(
    rows: list[str], index_permutations: list[list[tuple[int]]]
) -> list[list[str]]:
    possible_strings = []
    for i in range(len(rows)):
        row_strings = []
        for combo in index_permutations[i]:
            string_builder = list(rows[i])
            for index in combo:
                string_builder[index] = "#"
            current_string = "".join(string_builder)
            current_string = current_string.replace("?", ".")
            row_strings.append(current_string)
        possible_strings.append(row_strings)

    return possible_strings


def match_sequences(
    possible_strings: list[list[str]], sequences: list[list[int]]
) -> list[int]:
    sequence_matches = []
    for i in range(len(sequences)):
        expression = r"^[.]*"
        expression_builder = [f"#{{{span}}}" for span in sequences[i]]
        expression += "[.]+".join(expression_builder) + "[.]*$"
        num_matches = 0
        for current_string in possible_strings[i]:
            if re.match(expression, current_string):
                num_matches += 1
        sequence_matches.append(num_matches)
    return sequence_matches


# Part 2 - Dynamic Programming
# I don't have experience with dynamic programming so I used this
# For my first attempt at the solution
# https://github.com/fuglede/adventofcode/blob/master/2023/day12/solutions.py
#  Can be used for Part 1 as well, but I want to keep my own solution for reference above
#  Uses recursion and caching to adjust for the large string sizes and combinations
@cache
def string_crawl_num_matches(
    row: str, sequence: list[int], num_contiguous: int = 0
) -> [int]:
    if not row:
        return not sequence and not num_contiguous
    matches = 0
    if row[0] == "?":
        choices = ["#", "."]
    else:
        choices = row[0]
    for choice in choices:
        if choice == "#":
            # Keep going with current group
            matches += num_matches(row[1:], sequence, num_contiguous + 1)
        else:
            if num_contiguous:
                # If we're at the end of a contiguous sequence, look for next sequence
                if sequence and sequence[0] == num_contiguous:
                    matches += num_matches(row[1:], sequence[1:])
            else:
                # If we're not in a contiguous sequence, move to next character
                matches += num_matches(row[1:], sequence)
    return matches


# Ultimate solution:
# Wanted a more efficient version and found this
# https://gist.github.com/Nathan-Fenner/781285b77244f06cf3248a04869e7161
# Basic advantage is that it looks ahead and ends a match-sequence as soon as it is impossible
# rather than crawling through every character of the strings
@cache
def num_matches(row: str, sequence: list[int]) -> [int]:
    # If we're done with a row, but still have a sequence that hasn't been matched, that's a zero
    if not row:
        # But if we're done with both a row and set of sequences, that means we've matched the pattern, thats a one
        if not sequence:
            return 1
        return 0
    # If we've it a match, but there are still more `#` in the string, we don't actually have a match
    # but if there aren't, that's a full match
    if not sequence:
        for tile in row:
            if tile == "#":
                return 0
        return 1

    # If there aren't enough characters left in the process to make the pattern work, it's a zero already
    if len(row) < sum(sequence) + len(sequence) - 1:
        # line is not long enough for all of the runs
        return 0
    # standard "not in a pattern" case, just move on
    if row[0] == ".":
        return num_matches(row[1:], sequence)
    # If we find a match, lets just do a quick forward look rather than doing a whole recursion
    if row[0] == "#":
        s = sequence[0]
        for i in range(s):
            # If we see dots ahead, no match
            if i < len(row) and row[i] == ".":
                return 0
            # If we see `#` directly after of where the sequence is supposed to end, no match
        if s < len(row) and row[s] == "#":
            return 0
        # Otherwise, we have a match, begin evaluating the next sequence
        return num_matches(row[s + 1 :], sequence[1:])
    # This is our question-mark case, just make two calls to the function for each option
    return num_matches("#" + row[1:], sequence) + num_matches("." + row[1:], sequence)


if __name__ == "__main__":
    rows, sequences = process_input("./puzzle input.txt")
    # OG Part 1
    # possible_strings = get_possible_strings(rows, get_index_permutations(rows))
    # matches = match_sequences(possible_strings, sequences)
    # print(f"Part 1: {sum(matches)}")

    # Redone Part 1
    matches_recursive = [num_matches(rows[i], sequences[i]) for i in range(len(rows))]
    print(f"Part 1: {sum(matches_recursive)}")

    # Part 2
    matches_unfolded = [
        num_matches("?".join([rows[i]] * 5), sequences[i] * 5) for i in range(len(rows))
    ]
    print(f"Part 2: {sum(matches_unfolded)}")
