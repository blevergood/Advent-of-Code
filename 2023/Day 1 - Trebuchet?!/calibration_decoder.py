#!/usr/bin/env python3
import solution_part_1
import solution_part_2

def calibrate_document_1(document: str) -> int:
    f = open(document, "r")
    numbers = [solution_part_1.get_number(line) for line in f.readlines()]
    f.close()
    return sum(numbers)

def calibrate_document_2(document: str) -> int:
    f = open(document, "r")
    numbers = [solution_part_2.get_number(line) for line in f.readlines()]
    f.close()
    return sum(numbers)


if __name__ == "__main__":
    print("Part 1:", calibrate_document_1("./puzzle input.txt"))
    print("Part 2:", calibrate_document_2("./puzzle input.txt"))
