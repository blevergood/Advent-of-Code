#!/usr/bin/env python3
def handle_input(input: str) -> list[str]:
    f = open(input, "r")
    grid = f.read().split("\n")
    f.close()
    return grid


def get_start(grid: list[str]) -> (int, int):
    for y in range(len(grid)):
        x = grid[y].find("S")
        if x != -1:
            return (x, y)


def get_possible_tiles(
    grid: list[str], start: tuple[int, int], steps: int
) -> list[tuple[int, int]]:
    to_visit: list[tuple[int, int]] = [start]
    steps_taken = 0
    while steps_taken < steps:
        steps_taken += 1
        i = len(to_visit)
        for j in range(i):
            current_tile = to_visit.pop(0)
            curr_x, curr_y = current_tile
            for tile in [
                (curr_x - 1, curr_y),
                (curr_x + 1, curr_y),
                (curr_x, curr_y - 1),
                (curr_x, curr_y + 1),
            ]:
                x, y = tile
                if y in range(len(grid)):
                    if x in range(len(grid[y])):
                        if grid[y][x] != "#" and tile not in to_visit:
                            to_visit.append(tile)
    print(to_visit)
    return len(to_visit)

if __name__ == "__main__":
    grid = handle_input("puzzle input.txt")
    start = get_start(grid)
    print(f"Part 1: {get_possible_tiles(grid, start, 64)}")
