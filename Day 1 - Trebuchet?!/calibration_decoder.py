#!/usr/bin/env python3
import re

def get_number(input):
    numbers = re.findall('[0-9]', input)
    print(numbers)
    if numbers[0]:
        print(numbers[0] + ' ' + numbers[-1])
        return int(numbers[0] + numbers[-1])
    print(0)
    return 0

def calibrate_document(document):
    f = open(document, 'r')
    numbers = [get_number(line) for line in f.readlines()]
    f.close()
    return sum(numbers)

if __name__ == '__main__':
    print(calibrate_document('./puzzle input.txt'))
        