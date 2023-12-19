#!/usr/bin/env python3
from collections import OrderedDict


def handle_input(input: str) -> list[str]:
    f = open(input, "r")
    string_steps = f.read().strip("\n").strip().split(",")
    f.close()
    return string_steps


def encode_steps(steps: str) -> int:
    value = 0
    for step in steps:
        value = (value + ord(step)) * 17 % 256
    return value


def organize_boxes(steps: str) -> dict[str, OrderedDict[str, int]]:
    boxes = {key: OrderedDict() for key in range(256)}
    for step in steps:
        if "-" in step:
            label = step[:-1]
            box = encode_steps(label)
            if label in boxes[box]:
                # This should move everything behind up.
                boxes[box].pop(label)
        elif "=" in step:
            label, value = step.split("=")
            box = encode_steps(label)
            # Should put at end if not in
            # And modify in place if in
            boxes[box][label] = int(value)
    return boxes


def calculate_focusing_power(boxes: dict[str, OrderedDict[str, int]]) -> int:
    focusing_power = 0
    for i in boxes.keys():
        for slot in range(len(boxes[i].keys())):
            current_power = (i + 1) * (slot + 1) * boxes[i][list(boxes[i].keys())[slot]]
            focusing_power += current_power
    return focusing_power


if __name__ == "__main__":
    steps = handle_input("puzzle input.txt")
    encodings = [encode_steps(step) for step in steps]
    print(f"Part 1: {sum(encodings)}")

    boxes = organize_boxes(steps)
    focusing_power = calculate_focusing_power(boxes)
    print(f"Part 2: {focusing_power}")
