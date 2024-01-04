#!/usr/bin/env python3
import re
from collections.abc import Iterable, Callable


# Node
class Pipe:
    # Above
    def __init__(self, value, x, y) -> None:
        self.value = value
        self.x = x
        self.y = y
        shapes_to_dirs = {
            "|": {(0, -1), (0, 1)},
            "-": {(-1, 0), (1, 0)},
            "L": {(1, 0), (0, -1)},
            "J": {(-1, 0), (0, -1)},
            "7": {(-1, 0), (0, 1)},
            "F": {(1, 0), (0, 1)},
            "S": {(0, 1), (1, 0), (0, -1), (-1, 0)},
            ".": set(),
        }
        self.dirs = shapes_to_dirs[value]

    def __hash__(self) -> int:
        return hash("{self.value}{self.x}{self.y}")

    def __str__(self) -> str:
        return f"{(self.value, self.x, self.y)}"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: "Pipe") -> bool:
        if isinstance(other, Pipe):
            return self.value == other.value and self.x == other.x and self.y == other.y
        return NotImplemented

    def is_acceptable_match(self, other: "Pipe") -> bool:
        if isinstance(other, Pipe):
            return (
                (
                    other.x == self.x - 1
                    and other.y == self.y
                    and (-1, 0) in self.dirs
                    and (1, 0) in other.dirs
                )
                or (
                    other.x == self.x + 1
                    and other.y == self.y
                    and (1, 0) in self.dirs
                    and (-1, 0) in other.dirs
                )
                or (
                    other.y == self.y - 1
                    and other.x == self.x
                    and (0, -1) in self.dirs
                    and (0, 1) in other.dirs
                )
                or (
                    other.y == self.y + 1
                    and other.x == self.x
                    and (0, 1) in self.dirs
                    and (0, -1) in other.dirs
                )
            )
        return NotImplemented


# Graph
class Maze:
    def __init__(
        self, dimensions: dict[str, int], pipes: dict[int, list[Pipe]]
    ) -> None:
        self.pipes: list[pipes] = []
        self.dimensions = dimensions
        self.start: Pipe = None
        for key in pipes.keys():
            self.start = next((x for x in pipes[key] if x.value == "S"), None)
            if self.start is not None:
                break

        """
        Function to populate the map with nodes and adjacency lists
        Part 1
        
        We know from the examples and the puzzle input that the
        Starting node `S` will only have two characters that it's compatible
        i.e. it's either on an edge or surrounded on left/right by `|` characters
        etc.

        So we just have to find the first compatible node and then move forward.
        Every other character can only move two ways, so if we know which of those ways
        we're coming from, it just has to pull the node in from the other direction
        until it hits the starting node again.

        Using a list so that the points are already ordered for Part 2
        """
        self.pipes.append(self.start)
        for next_x, next_y in self.start.dirs:
            x, y = self.start.x + next_x, self.start.y + next_y
            if y in pipes.keys():
                if x < len(pipes[y]):
                    next_tile = pipes[y][x]
                    if self.start.is_acceptable_match(next_tile):
                        current_tile = next_tile
                        coming_from = {(-next_x, -next_y)}
                        break
        while current_tile != self.start:
            self.pipes.append(current_tile)
            next_x, next_y = list(current_tile.dirs - coming_from)[0]
            x, y = current_tile.x + next_x, current_tile.y + next_y
            coming_from = {(-next_x, -next_y)}
            current_tile = pipes[y][x]


# Part 1
def get_pipes(lines: list[str]) -> dict[int, list[Pipe]]:
    extractor = r"[.\|\-LJ7FS]"
    # dict of lists here to make it more performant
    return {
        i: [Pipe(m.group(0), m.start(), i) for m in re.finditer(extractor, lines[i])]
        for i in range(len(lines))
    }


def get_maze(input: str) -> Maze:
    f = open(input, "r")
    lines = f.read().split("\n")
    f.close()

    dimensions = {"x": len(lines[0]), "y": len(lines)}
    pipes = get_pipes(lines)
    return Maze(dimensions, pipes)


# Part 2
# Shoelace/Guass's area formula: https://en.wikipedia.org/wiki/Shoelace_formula
# Simplified: https://www.101computing.net/the-shoelace-algorithm/
# Calculates the area of a 2D shape based on the coordinates of the points (provided in order)
def get_area(ordered_points: list[Pipe]) -> int:
    return (
        abs(
            sum(
                [
                    ordered_points[i].x * ordered_points[i + 1].y
                    for i in range(len(ordered_points) - 1)
                ]
            )
            + (ordered_points[-1].x * ordered_points[0].y)
            - sum(
                [
                    ordered_points[i + 1].x * ordered_points[i].y
                    for i in range(len(ordered_points) - 1)
                ]
            )
            - ordered_points[0].x * ordered_points[-1].y
        )
        / 2
    )


# Picks Theorem: https://en.wikipedia.org/wiki/Pick%27s_theorem
# Relates the number of internal points (i.e. on a graph-paper) inside a shape
# to the shape's area and the number of external points
def get_interior_points(area: int, boundary_points: int) -> int:
    return area - (boundary_points / 2) + 1


if __name__ == "__main__":
    maze = get_maze("puzzle input.txt")
    pipes = maze.pipes

    # since connections can only make right-angle turns, there have to be an even number of pipes
    # So the furthest pipe will be the half-way point of the loop.
    print(f"Part 1: {len(pipes)/2}")

    print(
        f"Part 2: {get_interior_points(get_area(pipes), len(pipes))}"
    )
