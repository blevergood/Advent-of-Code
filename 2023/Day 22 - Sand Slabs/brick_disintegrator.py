#!/usr/bin/env python3
from collections import namedtuple
from collections.abc import Generator
from dataclasses import dataclass

Cube = namedtuple("Cube", ["x", "y", "z"])


# https://www.reddit.com/r/adventofcode/comments/18o7014/comment/kexg58r/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
@dataclass
class Brick:
    start: Cube
    end: Cube
    brick_id: int


def get_cubes(bricks: list[Brick], brick_id: int) -> Generator[Cube]:
    brick = bricks[brick_id]
    if brick.start.x != brick.end.x:
        for x in range(
            min(brick.start.x, brick.end.x), max(brick.start.x, brick.end.x) + 1
        ):
            yield (x, brick.start.y, brick.start.z)
    elif brick.start.y != brick.end.y:
        for y in range(
            min(brick.start.y, brick.end.y), max(brick.start.y, brick.end.y) + 1
        ):
            yield (brick.start.x, y, brick.start.z)
    # Will create a 1-cube brick if z isn't different
    else:
        for z in range(
            min(brick.start.z, brick.end.z), max(brick.start.z, brick.end.z) + 1
        ):
            yield (brick.start.x, brick.start.y, z)


def is_falling(
    grid: dict[tuple[int, int, int], int],
    bricks: list[Brick],
    brick: Brick,
    check_brick_id: int = -1,
):
    if brick.brick_id == check_brick_id:
        return False
    z = min(brick.start.z, brick.end.z)
    if z == 1:
        return False
    if brick.start.z != brick.end.z:
        below_brick_id = grid.get((brick.start.x, brick.start.y, z - 1))
        return below_brick_id in [None, check_brick_id]
    else:
        for x, y, z in get_cubes(bricks, brick.brick_id):
            below_brick_id = grid.get((x, y, z - 1))
            if below_brick_id not in [None, check_brick_id]:
                return False
        return True


def get_falling_bricks(
    grid: dict[tuple[int, int, int] : int],
    bricks: list[Brick],
    check_brick_id: int = -1,
) -> set[int]:
    falling_brick_ids = set()
    max_z = max(z for _, _, z in grid.keys())
    if check_brick_id == -1:
        min_z = 1
    else:
        min_z = max(bricks[check_brick_id].start.z, bricks[check_brick_id].end.z) + 1
    for z in range(min_z, max_z + 1):
        current_bricks = [
            brick for brick in bricks if z in [brick.start.z, brick.end.z]
        ]
        for brick in current_bricks:
            if is_falling(grid, bricks, brick, check_brick_id):
                falling_brick_ids.add(brick.brick_id)
                for x, y, z in get_cubes(bricks, brick.brick_id):
                    del grid[(x, y, z)]
                    grid[(x, y, z - 1)] = brick.brick_id
                if check_brick_id == -1:
                    brick.start = Cube(brick.start.x, brick.start.y, brick.start.z - 1)
                    brick.end = Cube(brick.end.x, brick.end.y, brick.end.z - 1)
    return falling_brick_ids


def drop_layers(grid: dict[tuple[int, int, int]], bricks: list[Brick]) -> None:
    while len(get_falling_bricks(grid, bricks)) > 0:
        pass


def get_removable_bricks(grid: dict[tuple[int, int, int]], bricks: list[Brick]) -> int:
    removable_bricks = 0
    for brick in bricks:
        grid_copy = grid.copy()
        falling_brick_ids = get_falling_bricks(grid, bricks, brick.brick_id)
        if len(falling_brick_ids) == 0:
            removable_bricks += 1
        grid = grid_copy
    return removable_bricks


def handle_input(input: str) -> (dict[tuple[int, int, int] : int], list[Brick]):
    f = open(input, "r")
    snapshot = f.read()
    f.close()
    bricks = []
    grid = dict()
    for line in snapshot.split("\n"):
        start, end = line.split("~")
        brick_start = Cube(*[int(coord) for coord in start.split(",")])
        brick_end = Cube(*[int(coord) for coord in end.split(",")])
        brick = Brick(brick_start, brick_end, len(bricks))
        bricks.append(brick)
        for x, y, z in get_cubes(bricks, brick.brick_id):
            grid[(x, y, z)] = brick.brick_id
    return grid, bricks


if __name__ == "__main__":
    grid, bricks = handle_input("puzzle input.txt")
    drop_layers(grid, bricks)
    removable_bricks = get_removable_bricks(grid, bricks)
    # TODO Find a faster method
    print(f"Part 1: {removable_bricks}")
