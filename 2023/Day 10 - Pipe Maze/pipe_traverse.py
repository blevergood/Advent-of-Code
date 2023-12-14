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
        shapes = {
            "|": ["above", "below"],
            "-": ["left", "right"],
            "L": ["above", "right"],
            "J": ["above", "left"],
            "7": ["left", "below"],
            "F": ["right", "below"],
            "S": ["above", "below", "right", "left"],
            ".": [],
        }
        self.shape = shapes[value]

    def __hash__(self) -> int:
        return hash("{self.value}{self.x}{self.y}")

    def __str__(self) -> str:
        return f"{(self.value, self.x, self.y)}"

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
                    and "left" in self.shape
                    and "right" in other.shape
                )
                or (
                    other.x == self.x + 1
                    and other.y == self.y
                    and "right" in self.shape
                    and "left" in other.shape
                )
                or (
                    other.y == self.y - 1
                    and other.x == self.x
                    and "above" in self.shape
                    and "below" in other.shape
                )
                or (
                    other.y == self.y + 1
                    and other.x == self.x
                    and "below" in self.shape
                    and "above" in other.shape
                )
            )
        return NotImplemented


# Graph
class Maze:
    def __init__(
        self, dimensions: dict[str, int], pipes: dict[int, list[Pipe]]
    ) -> None:
        self.pipes = dict()
        self.dimensions = dimensions
        self.start = None
        queue = []
        visited = []
        for key in pipes.keys():
            self.start = next((x for x in pipes[key] if x.value == "S"), None)
            if self.start is not None:
                break

        # Function to populate the map with nodes and adjacency lists
        queue.append(self.start)
        visited.append(self.start)
        while queue:
            a = queue.pop(0)
            for x, y in [
                (a.x + 1, a.y),
                (a.x - 1, a.y),
                (a.x, a.y + 1),
                (a.x, a.y - 1),
            ]:
                if y in pipes.keys():
                    if x < len(pipes[y]):
                        neighbor = pipes[y][x]
                        if a.is_acceptable_match(neighbor):
                            if neighbor not in visited:
                                visited.append(neighbor)
                                queue.append(neighbor)
                            if a in self.pipes:
                                self.pipes[a].append(neighbor)
                            else:
                                self.pipes[a] = [neighbor]


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


if __name__ == "__main__":
    maze = get_maze("./puzzle input.txt")
    pipes = maze.pipes
    # since connections can only make right-angle turns, there have to be an even number of pipes
    # So the furthest pipe will be the half-way point of the loop.
    print(f"Part 1: {len(pipes)/2}")
