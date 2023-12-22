#!/usr/bin/env python3
def handle_input(input: str) -> list[tuple[str, int, str]]:
    f = open(input, "r")
    dig_steps = f.read().split("\n")
    dig_plan = []
    for step in dig_steps:
        direction, distance, color = step.split(" ")
        dig_plan.append((direction, int(distance), color[1:-1]))
    return dig_plan


def get_lagoon_points(
    dig_plan: list[tuple[str, int, str]]
) -> list[tuple[int, int, str]]:
    plan_dispatch = {
        "R": lambda x, y, distance: (x + distance, y),
        "L": lambda x, y, distance: (x - distance, y),
        "D": lambda x, y, distance: (x, y + distance),
        "U": lambda x, y, distance: (x, y - distance),
    }
    previous_coords = (0, 0, "")
    lagoon_points = [previous_coords]
    for step in dig_plan:
        current_coords = plan_dispatch[step[0]](*previous_coords[:2], step[1])
        current_coords += (step[2],)
        if previous_coords[0] == current_coords[0]:
            if previous_coords[1] < current_coords[1]:
                intermediate_points = [
                    (current_coords[0], previous_coords[1] + i, current_coords[2])
                    for i in range(1, current_coords[1] - previous_coords[1])
                ]
            elif previous_coords[1] > current_coords[1]:
                intermediate_points = [
                    (current_coords[0], previous_coords[1] - i, current_coords[2])
                    for i in range(1, previous_coords[1] - current_coords[1])
                ]
        elif previous_coords[1] == current_coords[1]:
            if previous_coords[0] < current_coords[0]:
                intermediate_points = [
                    (previous_coords[0] + i, current_coords[1], current_coords[2])
                    for i in range(1, current_coords[0] - previous_coords[0])
                ]
            elif previous_coords[0] > current_coords[0]:
                intermediate_points = [
                    (previous_coords[0] - i, current_coords[1], current_coords[2])
                    for i in range(1, previous_coords[0] - current_coords[0])
                ]
        lagoon_points.extend(intermediate_points)
        if current_coords[:2] != (0, 0):
            lagoon_points.append(current_coords)
        previous_coords = current_coords
    return lagoon_points


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
    dig_plan = handle_input("puzzle input.txt")
    # For part 1, we can track the diff's for number of points, rather than generating all of the points and counting
    # Keeping it for now bc I assume the color will come into play

    # boundary points
    lagoon_points = get_lagoon_points(dig_plan)

    # Area based on shoelace formula, see Day 10
    lagoon_area = get_area([lagoon_point[:2] for lagoon_point in lagoon_points])
    # Distinct points based on area and number of boundary points (also Day 10)
    int_points = get_interior_points(lagoon_area, len(lagoon_points))

    print(f"Part 1: {int(len(lagoon_points) + int_points)}")
