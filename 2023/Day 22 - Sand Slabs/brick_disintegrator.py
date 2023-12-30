#!/usr/bin/env python3
# Adapted from https://github.com/MeisterLLD/aoc2023/blob/main/22.py
def handle_input(input: str) -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    f = open(input, "r")
    snapshot = f.read()
    f.close()
    bricks = []
    for line in snapshot.split("\n"):
        start, end = line.split("~")
        x1, y1, z1 = (int(coord) for coord in start.split(","))
        x2, y2, z2 = (int(coord) for coord in end.split(","))
        bricks.append(((x1, y1, z1), (x2, y2, z2)))
        bricks = sorted(bricks, key=lambda x: x[0][2])
    return bricks


def get_tiles(
    brick: tuple[tuple[int, int, int], tuple[int, int, int]]
) -> list[tuple[int, int, int]]:
    start, end = brick

    if start[0] != end[0]:
        return [(x, start[1], start[2]) for x in range(start[0], end[0] + 1)]
    if start[1] != end[1]:
        return [(start[0], y, start[2]) for y in range(start[1], end[1] + 1)]
    if start[2] != end[2]:
        return [(start[0], start[1], z) for z in range(start[2], end[2] + 1)]
    return [start]


def can_fall(
    brick: tuple[tuple[int, int, int], tuple[int, int, int]],
    occupied_spaces: set[tuple[int, int, int]],
) -> bool:
    return all(tile not in occupied_spaces for tile in get_tiles(brick))


def get_settled_bricks(
    bricks: list[tuple[tuple[int, int, int], tuple[int, int, int]]]
) -> (
    list[tuple[tuple[int, int, int], tuple[int, int, int]]],
    set[tuple[int, int, int]],
):
    new_bricks = []
    occupied_spaces = set()
    for brick in bricks:
        start, end = brick
        x1, y1, z1 = start
        x2, y2, z2 = end
        while (
            can_fall(((x1, y1, z1 - 1), (x2, y2, z2 - 1)), occupied_spaces)
            and z1 - 1 >= 1
        ):
            z1 -= 1
            z2 -= 1
        new_brick = ((x1, y1, z1), (x2, y2, z2))
        new_bricks.append(new_brick)
        for tile in get_tiles(new_brick):
            occupied_spaces.add(tile)
        new_bricks = sorted(new_bricks, key=lambda x: x[0][2])
    return new_bricks, occupied_spaces


def supports(
    brick_1: tuple[tuple[int, int, int], tuple[int, int, int]],
    brick_2: tuple[tuple[int, int, int], tuple[int, int, int]],
) -> bool:
    for tile in get_tiles(brick_1):
        x, y, z = tile
        if (x, y, z + 1) in get_tiles(brick_2):
            return True
    return False


def get_disintegration_graph(
    bricks: tuple[tuple[int, int, int], tuple[int, int, int]]
) -> dict[int:int]:
    parents = {i: [] for i in range(len(bricks))}
    children = {i: [] for i in range(len(bricks))}
    disintegration_graph = {i: [] for i in range(len(bricks))}
    for i, brick_1 in enumerate(bricks):
        for j, brick_2 in enumerate(bricks):
            if brick_2[0][2] > brick_1[1][2] + 1:
                break
            if j > i and supports(brick_1, brick_2):
                parents[j].append(i)
                children[i].append(j)
    for i in range(len(bricks)):
        for j in range(len(bricks)):
            # Get the blocks that are only supported by exactly 1 other block
            if parents[j] == [i]:
                disintegration_graph[i].append(j)
    return disintegration_graph


if __name__ == "__main__":
    bricks = handle_input("puzzle input.txt")
    settled_bricks, occupied_spaces = get_settled_bricks(bricks)
    disintegration_graph = get_disintegration_graph(settled_bricks)
    print(f"Part 1: {sum(disintegration_graph[i] == [] for i in range(len(bricks)))}")
