#!/usr/bin/env python3#!/usr/bin/env python3
import re
from itertools import combinations


def process_input(input: str) -> (list[str], list[int]):
    f = open(input, "r")
    lines = f.read().split("\n")
    f.close()

    rows, sequences = [], []
    for line in lines:
        row, seq_str = line.split(" ")
        seq = [int(n) for n in seq_str.split(",")]
        rows.append(row)
        sequences.append(seq)
    return rows, sequences


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


if __name__ == "__main__":
    rows, sequences = process_input("./puzzle input.txt")
    possible_strings = get_possible_strings(rows, get_index_permutations(rows))
    matches = match_sequences(possible_strings, sequences)
    print(f"Part 1: {sum(matches)}")
