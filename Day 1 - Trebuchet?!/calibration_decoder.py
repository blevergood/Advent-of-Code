#!/usr/bin/env python3
# from solution_1 import get_number
from solution_2 import get_number

def calibrate_document(document):
    f = open(document, "r")
    numbers = [get_number(line) for line in f.readlines()]
    f.close()
    return sum(numbers)


if __name__ == "__main__":
    print(calibrate_document("./puzzle input.txt"))
