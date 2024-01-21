#!/usr/bin/env python3
from collections.abc import Callable
from keyword import iskeyword, issoftkeyword
import re


def handle_input(input: str) -> (str, str):
    f = open(input, "r")
    workflows_str, parts_str = f.read().split("\n\n")
    f.close()
    return workflows_str, parts_str


# Part 1
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


# Part 2
# https://github.com/JoanaBLate/advent-of-code-js/blob/main/2023/day19/solve2.js
def create_range():
    return {part: {"low": 1, "high": 4000} for part in ["x", "m", "a", "s"]}


def parse_condition(raw_condition: str) -> dict[str, str | int]:
    if ":" not in raw_condition:
        part, operator, operand, destination = "", "", 0, raw_condition
    else:
        part, operator, operand, destination = (
            raw_condition[0],
            raw_condition[1],
            int(raw_condition[2 : raw_condition.find(":")]),
            raw_condition[raw_condition.find(":") + 1 :],
        )
    return {
        "part": part,
        "operator": operator,
        "operand": operand,
        "destination": destination,
        "range": create_range(),
    }


def get_workflow_conditions(workflow_str: str) -> dict[str, list[dict[str, str | int]]]:
    workflow_conditions = {}
    for workflow in workflow_str.split("\n"):
        func_name = workflow[: workflow.find("{")]
        raw_conditions = workflow[workflow.find("{") + 1 : -1].split(",")
        conditions = [parse_condition(condition) for condition in raw_conditions]
        workflow_conditions[func_name] = conditions
    return workflow_conditions


def clone_range(range: dict[str, dict[str, int]]) -> dict[str, dict[str, int]]:
    clone = create_range()
    for part in ["x", "m", "a", "s"]:
        clone[part]["low"] = range[part]["low"]
        clone[part]["high"] = range[part]["high"]
    return clone


def increment_range(range: dict[str, dict[str, int]]) -> int:
    result = 1
    for part in ["x", "m", "a", "s"]:
        result *= range[part]["high"] - range[part]["low"] + 1
    return result


def update_sub_range(
    operator: str,
    operand: int,
    sub_range: dict[str, int],
    new_sub_range: dict[str, int],
) -> None:
    if operator == "<":
        new_sub_range["high"] = operand - 1
        sub_range["low"] = operand
    elif operator == ">":
        new_sub_range["low"] = operand + 1
        sub_range["high"] = operand


def process_condition(
    workflow_conditions: dict[str, list[dict[str, str | int]]],
    range: dict[str, dict[str, int]],
    condition: dict[str, str | int],
    total: int,
) -> int:
    condition["range"] = clone_range(range)
    new_range = clone_range(condition["range"])
    if condition["part"] in ["x", "m", "a", "s"]:
        update_sub_range(
            condition["operator"],
            condition["operand"],
            condition["range"][condition["part"]],
            new_range[condition["part"]],
        )
    if condition["destination"] == "R":
        return total
    if condition["destination"] == "A":
        total += increment_range(new_range)
        return total
    return walk(condition["destination"], workflow_conditions, new_range, total)


def walk(
    workflow_name: str,
    workflow_conditions: dict[str, list[dict[str, str | int]]],
    range: dict[str, dict[str, int]],
    total: int,
) -> int:
    for condition in workflow_conditions[workflow_name]:
        total = process_condition(workflow_conditions, range, condition, total)
        range = condition["range"]
    return total


if __name__ == "__main__":
    workflows_str, parts_str = handle_input("puzzle input.txt")
    workflows, parts = generate_workflows(workflows_str, parts_str)
    print(f"Part 1: {calculate_parts(workflows, parts)}")

    workflow_conditions = get_workflow_conditions(workflows_str)
    total = walk("in", workflow_conditions, create_range(), 0)
    print(f"Part 2: {total}")
