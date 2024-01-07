#!/usr/bin/env python3
def handle_input(input: str) -> list[str]:
    f = open(input, "r")
    grid = f.read().split("\n")
    f.close()
    return grid


def get_border_beams(grid: list[str]) -> set[tuple[int, int, int, int]]:
    border_beams = set()
    for y in range(len(grid)):
        border_beams.update({(-1, y, 1, 0), (len(grid[0]), y, -1, 0)})
    for x in range(len(grid[0])):
        border_beams.update({(x, -1, 0, 1), (x, len(grid), 0, -1)})
    return border_beams


def traverse_floor(
    grid: list[str], start: tuple[int, int, int, int]
) -> set[tuple[int, int]]:
    queue = [start]
    seen = set()

    while queue:
        x, y, dx, dy = queue.pop(0)
        x += dx
        y += dy
        if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
            new_pos = grid[y][x]
            if (new_pos == "-" and dy != 0) or (new_pos == "|" and dx != 0):
                for d_x, d_y in (
                    [(0, 1), (0, -1)] if new_pos == "|" else [(1, 0), (-1, 0)]
                ):
                    if (x, y, d_x, d_y) not in seen:
                        queue.append((x, y, d_x, d_y))
                        seen.add((x, y, d_x, d_y))
            else:
                if new_pos == "\\":
                    dx, dy = dy, dx
                elif new_pos == "/":
                    dx, dy = -dy, -dx

                if (x, y, dx, dy) not in seen:
                    queue.append((x, y, dx, dy))
                    seen.add((x, y, dx, dy))
    visited = {(x, y) for (x, y, _, _) in seen}
    return visited


if __name__ == "__main__":
    grid = handle_input("puzzle input.txt")
    visited = traverse_floor(grid, (-1, 0, 1, 0))
    print(f"Part 1: {len(visited)}")

    border_beams = get_border_beams(grid)
    all_visited = [len(traverse_floor(grid, start)) for start in border_beams]
    print(f"Part 2: {max(all_visited)}")
