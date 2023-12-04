#!/usr/bin/env python3
import re


def get_number(input):
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


def calibrate_document(document):
    f = open(document, "r")
    numbers = [get_number(line) for line in f.readlines()]
    f.close()
    return sum(numbers)


if __name__ == "__main__":
    print(calibrate_document("./puzzle input.txt"))
