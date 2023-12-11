#!/usr/bin/env python3
import re


# Part 1
def get_number_int(input: str) -> int:
    numbers = re.findall("[1-9]", input)
    if numbers[0]:
        return int(numbers[0] + numbers[-1])
    return 0


def calibrate_document_int(document: str) -> int:
    f = open(document, "r")
    numbers = [get_number_int(line) for line in f.readlines()]
    f.close()
    return sum(numbers)


# Part 2
def get_number_alpha_num(input: str) -> int:
    number_map = {
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    matches = re.finditer(
        r"(?=([1-9]|one|two|three|four|five|six|seven|eight|nine))", input
    )
    numbers = [match.group(1) for match in matches]
    if numbers[0]:
        return int(number_map[numbers[0]] + number_map[numbers[-1]])
    return 0


def calibrate_document_alpha_num(document: str) -> int:
    f = open(document, "r")
    numbers = [get_number_alpha_num(line) for line in f.readlines()]
    f.close()
    return sum(numbers)


if __name__ == "__main__":
    print("Part 1:", calibrate_document_int("./puzzle input.txt"))
    print("Part 2:", calibrate_document_alpha_num("./puzzle input.txt"))
