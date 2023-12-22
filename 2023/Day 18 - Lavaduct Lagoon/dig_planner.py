#!/usr/bin/env python3
def handle_input(input: str, part_2: bool = False) -> list[tuple[str, int, str]]:
    f = open(input, "r")
    dig_steps = f.read().split("\n")
    dig_plan = []
    for step in dig_steps:
        if not part_2:
            direction, distance = step.split(" ")[:2]
        else:
            direction_converter = ["R", "D", "L", "U"]
            # last item of the list, strip `(`, `#`, and `)`
            code = step.split(" ")[-1][2:-1]
            direction, distance = direction_converter[int(code[-1])], int(code[:-1], 16)
        dig_plan.append((direction, int(distance)))
    return dig_plan


def get_lagoon_points(
    dig_plan: list[tuple[str, int, str]]
) -> (list[tuple[int, int]], int):
    plan_dispatch = {
        "R": lambda x, y, distance: (x + distance, y),
        "D": lambda x, y, distance: (x, y + distance),
        "L": lambda x, y, distance: (x - distance, y),
        "U": lambda x, y, distance: (x, y - distance),
    }
    previous_coords = (0, 0)
    lagoon_points = [previous_coords]
    border_size = 1
    for step in dig_plan:
        current_coords = plan_dispatch[step[0]](*previous_coords[:2], step[1])
        if previous_coords[0] == current_coords[0]:
            border_size += abs(previous_coords[1] - current_coords[1])
        elif previous_coords[1] == current_coords[1]:
            border_size += abs(previous_coords[0] - current_coords[0])
        if current_coords != (0, 0):
            lagoon_points.append(current_coords)
        else:
            border_size -= 1
        previous_coords = current_coords
    return lagoon_points, border_size


# Shoelace/Guass's area formula: https://en.wikipedia.org/wiki/Shoelace_formula
# Simplified: https://www.101computing.net/the-shoelace-algorithm/
# Calculates the area of a 2D shape based on the coordinates of the points (provided in order)
def get_area(ordered_points: list[tuple[int, int]]) -> int:
    return (
        abs(
            sum(
                [
                    ordered_points[i][0] * ordered_points[i + 1][1]
                    for i in range(len(ordered_points) - 1)
                ]
            )
            + (ordered_points[-1][0] * ordered_points[0][1])
            - sum(
                [
                    ordered_points[i + 1][0] * ordered_points[i][1]
                    for i in range(len(ordered_points) - 1)
                ]
            )
            - ordered_points[0][0] * ordered_points[-1][1]
        )
        / 2
    )


def get_interior_points(area: int, boundary_points: int) -> int:
    return area - (boundary_points / 2) + 1


if __name__ == "__main__":
    input = "puzzle input.txt"
    # Part 1
    dig_plan_1 = handle_input(input)
    # boundary points
    lagoon_points_1, border_size_1 = get_lagoon_points(dig_plan_1)
    # Area based on shoelace formula, see Day 10
    lagoon_area_1 = get_area([lagoon_point for lagoon_point in lagoon_points_1])
    # Distinct points based on area and number of boundary points (also Day 10)
    int_points_1 = get_interior_points(lagoon_area_1, border_size_1)
    print(f"Part 1: {int(border_size_1 + int_points_1)}")

    # Part 2
    dig_plan_2 = handle_input(input, True)
    lagoon_points_2, border_size_2 = get_lagoon_points(dig_plan_2)
    lagoon_area_2 = get_area([lagoon_point for lagoon_point in lagoon_points_2])
    int_points_2 = get_interior_points(lagoon_area_2, border_size_2)
    print(f"Part 2: {int(border_size_2 + int_points_2)}")
