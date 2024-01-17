#!/usr/bin/env python3
from collections.abc import Callable
from keyword import iskeyword, issoftkeyword
import re


def handle_input(input: str) -> (str, str):
    f = open(input, "r")
    workflows_str, parts_str = f.read().split("\n\n")
    f.close()
    return workflows_str, parts_str


# Create functions using `exec` to build strings with the appropriate logic
def generate_workflows(
    workflows_str: str, parts_str: str
) -> (dict[str, Callable[[dict[str, int]], str]], dict[str, int]):
    workflows = {}
    for workflow in workflows_str.split("\n"):
        func_name = workflow[: workflow.find("{")]
        if iskeyword(func_name) or issoftkeyword(func_name):
            func_name += "_"
        str_builder = [f"def {func_name}(part):"]
        conditions = workflow[workflow.find("{") + 1 : -1].split(",")

        for i in range(len(conditions)):
            if ":" not in conditions[i]:
                outcome = conditions[i]
                indent = ""
            else:
                expression, outcome = conditions[i].split(":")
                str_builder.append(f"\n    if part['{expression[0]}']{expression[1:]}:")
                indent = "    "
            if outcome in ["A", "R"]:
                str_builder.append(f"\n{indent}    return '{outcome}'")
            else:
                str_builder.append(f"\n{indent}    return workflows['{outcome}'](part)")
        str_builder.append(f"\nworkflows['{func_name}'] = {func_name}")
        exec("".join(str_builder))
    # Create dict from string with dict appearance (i.e. "{a: 1, a: 2}")
    parts = [
        eval(
            part.replace("=", ":")
            .replace("x", "'x'")
            .replace("m", "'m'")
            .replace("a", "'a'")
            .replace("s", "'s'")
        )
        for part in parts_str.split("\n")
    ]
    return workflows, parts


def calculate_parts(
    workflows: dict[str, Callable[[dict[str, int]], str]], parts: dict[str, int]
) -> int:
    total_sum = 0
    for part in parts:
        if workflows["in_"](part) == "A":
            total_sum += sum(part.values())
    return total_sum


def get_total_approved(
    workflows_str: str, workflows: dict[str, Callable[[dict[str, int]], str]]
) -> int:
    # Get all the ranges addressed by the functions
    splits = {category: [0, 4000] for category in "xmas"}
    for category, operator, value in re.findall(r"(\w+)(<|>)(\d+)", workflows_str):
        splits[category].append(int(value) - (operator == "<"))

    ranges = lambda x: [(a, a - b) for a, b in zip(x[1:], x)]

    # Test all the combinations of all the ranges
    # As opposed to every possible input.
    # (See Day 5)
    # Takes about 15 minutes to run
    # TODO: Make this more efficient
    X, M, A, S = [ranges(sorted(splits[x])) for x in splits]
    total_approved = 0
    for x, dx in X:
        for m, dm in M:
            for a, da in A:
                for s, ds in S:
                    total_approved += (
                        dx
                        * dm
                        * da
                        * ds
                        * bool(
                            workflows["in_"]({"x": x, "m": m, "a": a, "s": s}) == "A"
                        )
                    )
    return total_approved


if __name__ == "__main__":
    workflows_str, parts_str = handle_input("puzzle input.txt")
    workflows, parts = generate_workflows(workflows_str, parts_str)
    print(f"Part 1: {calculate_parts(workflows, parts)}")
    print(f"Part 2: {get_total_approved(workflows_str, workflows)}")
