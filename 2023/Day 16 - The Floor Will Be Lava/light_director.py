#!/usr/bin/env python3
import re


def handle_input(input: str) -> list[str]:
    f = open(input, "r")
    grid = f.read().split("\n")
    f.close()
    return grid


def get_border_beams(grid: list[str]) -> set[tuple[int, int, int, int]]:
    border_beams = set()
    for y in range(len(grid)):
        border_beams.update({(0, y, 1, 0), (len(grid[0]) - 1, y, -1, 0)})
    for x in range(len(grid[0])):
        border_beams.update({(x, 0, 0, 1), (x, len(grid) - 1, 0, -1)})
    return border_beams


# Create a list of vertices and edges so that we only have edges and special characters
# Each vertex is of the format: {tuple[int, int]: dict[str, tuple[int, int]}
# Where each tuple is a "decision tile" coordinate, and the `str` entries for each vertex is "top," "right", "bottom", "left" as long as those edges exist
# so that we can jump between points where we have to make decisions, rather than crawling through all points
# "|.../" -> {(0, 0): {"right": (0, 5)}} etc.
def compress_floor(
    grid: list[str],
) -> dict[tuple[int, int], dict[tuple[int, int], tuple[int, int]]]:
    # dirs = {(0, -1): "top", (1, 0): "right", (0, 1): "bottom", (-1, 0): "left"}
    
    # a `vertex` is (`/`, `\`, `-`, `|`) tiles & border tiles (which can be `.` tiles)
    vertices = {
        (x, y): dict()
        for y in range(len(grid))
        for x in range(len(grid[y]))
        if grid[y][x] != "."
        or (x == 0 or x == len(grid[0]) - 1)
        or (y == 0 or y == len(grid) - 1)
    }
    for x, y in vertices.keys():
        if x < len(grid) - 1:
            right = re.search(r"[^.-]", grid[y][x + 1 :])
            if right is None:
                right = len(grid) - 1
            else:
                right = right.start() + x + 1
            vertices[(x, y)][(1, 0)] = (right, y)
        if x > 0:
            left = re.search(r"[^.-]", "".join(reversed(grid[y][:x])))
            if left is None:
                left = 0
            else:
                left = x - left.start() - 1
            vertices[(x, y)][(-1, 0)] = (left, y)
        if y < len(grid) - 1:
            lower = ("").join(grid[i][x] for i in range(y + 1, len(grid)))
            bottom = re.search(r"[^.|]", lower)
            if bottom is None:
                bottom = len(grid) - 1
            else:
                bottom = bottom.start() + y + 1
            vertices[(x, y)][(0, 1)] = (x, bottom)
        if y > 0:
            upper = "".join([grid[y - i][x] for i in range(1, y)])
            top = re.search(r"[^.|]", upper)
            if top is None:
                top = 0
            else:
                top = y - top.start() - 1
            vertices[(x, y)][(0, -1)] = (x, top)
    return vertices


def turn(
    grid: list[str], start: tuple[int, int, int, int]
) -> tuple[int, int, int, int]:
    next_tiles = []
    x, y, dx, dy = start
    pos = grid[y][x]
    if (pos == "-" and dy != 0) or (pos == "|" and dx != 0):
        for d_x, d_y in [(0, 1), (0, -1)] if pos == "|" else [(1, 0), (-1, 0)]:
            next_tiles.append((x, y, d_x, d_y))
    else:
        if pos == "\\":
            dx, dy = dy, dx
        elif pos == "/":
            dx, dy = -dy, -dx
        next_tiles.append((x, y, dx, dy))
    return next_tiles


def traverse_floor(
    grid: list[str],
    vertices: dict[tuple[int, int], dict[str, tuple[int, int]]],
    start: tuple[int, int, int, int],
) -> set[tuple[int, int]]:
    # dirs = {(0, -1): "top", (1, 0): "right", (0, 1): "bottom", (-1, 0): "left"}

    # Account for starting on a tile that isn't a `.`
    start_tiles = turn(grid, start)
    queue = [s for s in start_tiles]
    seen = {s for s in start_tiles}
    while queue:
        # Get vertex
        x, y, dx, dy = queue.pop(0)
        if (dx, dy) not in vertices[(x, y)]:
            continue
        new_x, new_y = vertices[(x, y)][(dx, dy)]
        if dy != 0:
            if dy > 0:
                y_range = range(y, new_y)
            elif dy < 0:
                y_range = reversed(range(new_y + 1, y))
            for i in y_range:
                # Performance improvement by checking midpoints against just
                # the two points
                mid = (x, i)
                if mid not in seen:
                    seen.add(mid)
        if dx != 0:
            if dx > 0:
                x_range = range(x, new_x)
            elif dx < 0:
                x_range = reversed(range(new_x + 1, x))
            for i in x_range:
                mid = (i, y)
                if mid not in seen:
                    seen.add(mid)
        next_tiles = turn(grid, (new_x, new_y, dx, dy))
        for tile in next_tiles:
            x, y, dx, dy = tile
            vertex = (x, y, dx, dy)
            if vertex not in seen:
                queue.append(tile)
                seen.add(vertex)
    visited = {(*s[:2],) for s in seen}
    return visited


# Fun visualization function to create traversals like from the example
def visualize(file, grid, visited):
    for x, y in visited:
        row_list = list(grid[y])
        row_list[x] = "#"
        grid[y] = "".join(row_list)
    f = open(f"visualization_{file}", "w+")
    for line in grid:
        f.write(f"{line}\n")
    f.close()


if __name__ == "__main__":
    grid = handle_input("puzzle input.txt")
    vertices = compress_floor(grid)
    visited = traverse_floor(grid, vertices, (0, 0, 1, 0))
    print(f"Part 1: {len(visited)}")

    # visualize("example.txt", grid, visited)

    border_beams = get_border_beams(grid)
    all_visited = [len(traverse_floor(grid, vertices, start)) for start in border_beams]
    print(f"Part 2: {max(all_visited)}")
