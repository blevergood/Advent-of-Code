import re

def get_number(input):
    numbers = re.findall('[1-9]', input)
    if numbers[0]:
        return int(numbers[0] + numbers[-1])
    return 0
