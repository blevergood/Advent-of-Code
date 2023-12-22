#!/usr/bin/env python3
from heapq import heappop, heappush
from sys import maxsize


def handle_input(input: str) -> list[list[int]]:
    f = open(input, "r")
    content = f.read().strip().split("\n")
    f.close()
    return [[int(n) for n in line] for line in content]


def minimal_heat_loss(
    grid: list[list[int]], min_distance: int, max_distance: int
) -> int:
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    # heat_loss, x, y, blocked_direction
    queue = [(0, 0, 0, -1)]
    seen = set()
    heat_loss_map = dict()
    while queue:
        heat_loss, x, y, blocked_direction = heappop(queue)
        # Return on reaching the bottom-left corner
        if x == len(grid) - 1 and y == len(grid[0]) - 1:
            return heat_loss
        if (x, y, blocked_direction) not in seen:
            seen.add((x, y, blocked_direction))
            for direction in range(len(directions)):
                # print(direction)
                more_heat_loss = 0
                if (
                    direction != blocked_direction
                    and ((direction + 2) % 4) != blocked_direction
                ):
                    for distance in range(1, max_distance + 1):
                        current_x = x + directions[direction][0] * distance
                        current_y = y + directions[direction][1] * distance
                        if current_x in range(len(grid)) and current_y in range(
                            len(grid[0])
                        ):
                            more_heat_loss += grid[current_x][current_y]
                            if distance >= min_distance:
                                new_heat_loss = heat_loss + more_heat_loss
                                if (
                                    heat_loss_map.get(
                                        (current_x, current_y, direction),
                                        maxsize,
                                    )
                                    > new_heat_loss
                                ):
                                    heat_loss_map[
                                        (current_x, current_y, direction)
                                    ] = new_heat_loss
                                    heappush(
                                        queue,
                                        (
                                            new_heat_loss,
                                            current_x,
                                            current_y,
                                            direction,
                                        ),
                                    )


if __name__ == "__main__":
    grid = handle_input("puzzle input.txt")
    print(f"Part 1: {minimal_heat_loss(grid, 1, 3)}")
    print(f"Part 2: {minimal_heat_loss(grid, 4, 10)}")
