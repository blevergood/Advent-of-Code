#!/usr/bin/env python3
from copy import deepcopy


class Tile:
    def __init__(
        self, value: str, x: int, y: int, grid_pos: str, energized: bool = False
    ) -> None:
        self.value = value
        self.x = x
        self.y = y
        self.energized = energized
        self.grid_pos = grid_pos
        mirror_turns = {
            "/": {"right": "up", "left": "down", "down": "left", "up": "right"},
            "\\": {"right": "down", "left": "up", "down": "right", "up": "left"},
        }
        if self.value in mirror_turns.keys():
            self.turns = mirror_turns[self.value]
        else:
            self.turns = None


class Floor:
    def __init__(self, tiles_str: list[list[str]]) -> None:
        self.height = len(tiles_str)
        self.width = len(tiles_str[0])
        self.size = self.height * self.width
        self.tiles = []
        for i in range(self.height):
            y_pos = ""
            current_row = []
            if i == 0:
                y_pos = "top"
            elif i == self.height - 1:
                y_pos = "bottom"
            for j in range(self.width):
                x_pos = ""
                if j == 0:
                    x_pos = "left"
                elif j == self.width - 1:
                    x_pos = "right"
                else:
                    x_pos = "mid"
                current_row.append(Tile(tiles_str[i][j], j, i, y_pos + x_pos, False))
            self.tiles.append(current_row)

    def tileAt(self, x: int, y: int) -> Tile:
        return self.tiles[y][x]

    def get_border(self) -> set(tuple[int, int]):
        border_coords = set()
        for y in range(self.height):
            if y == 0 or y == self.height - 1:
                for x in range(self.width):
                    border_coords.add((x, y))
            else:
                border_coords.update([(0, y), (self.width - 1, y)])
        return border_coords

    def get_energized(self) -> list[Tile]:
        energized_tiles = []
        for row in self.tiles:
            for tile in row:
                if tile.energized:
                    energized_tiles.append(tile)
        return energized_tiles


class Beam:
    def __init__(self, floor: Floor, x: int, y: int, direction: str) -> None:
        self.x = x
        self.y = y
        self.floor = floor
        self.direction = direction
        self.current_tile = self.floor.tileAt(self.x, self.y)
        self.current_tile.energized = True
        if self.current_tile.value == "|" and self.direction in ["left", "right"]:
            self.split = "vertical"
            self.done = True
        elif self.current_tile.value == "-" and self.direction in ["up", "down"]:
            self.split = "horizontal"
            self.done = True
        else:
            self.split = ""
            self.done = False

    def move_right(self) -> None:
        if "right" not in self.current_tile.grid_pos:
            self.x += 1

    def move_left(self) -> None:
        if "left" not in self.current_tile.grid_pos:
            self.x -= 1

    def move_up(self) -> None:
        if "top" not in self.current_tile.grid_pos:
            self.y -= 1

    def move_down(self) -> None:
        if "bottom" not in self.current_tile.grid_pos:
            self.y += 1

    def move(self) -> None:
        options = {
            "right": self.move_right,
            "left": self.move_left,
            "up": self.move_up,
            "down": self.move_down,
        }

        options[self.direction]()
        self.current_tile = self.floor.tileAt(self.x, self.y)
        self.current_tile.energized = True
        if self.current_tile.value == "|" and (
            self.direction == "left" or self.direction == "right"
        ):
            self.split = "vertical"
            self.done = True
        elif self.current_tile.value == "-" and (
            self.direction == "up" or self.direction == "down"
        ):
            self.split = "horizontal"
            self.done = True
        elif self.current_tile.turns is not None:
            self.direction = self.current_tile.turns[self.direction]

        if (
            (self.direction == "left" and "left" in self.current_tile.grid_pos)
            or (self.direction == "right" and "right" in self.current_tile.grid_pos)
            or (self.direction == "up" and "top" in self.current_tile.grid_pos)
            or (self.direction == "down" and "bottom" in self.current_tile.grid_pos)
        ):
            self.done = True


def handle_input(input: str) -> list[list[str]]:
    f = open(input, "r")
    tiles_str = [list(row) for row in f.read().split("\n")]
    f.close()
    return tiles_str


def traverse_floor(
    floor: Floor,
    start: tuple[int, int] = (0, 0),
    direction: str = "right",
) -> Floor:
    trav_floor = deepcopy(floor)
    # Need to account for if the first tile itself is a mirror
    if trav_floor.tileAt(*start).value in ["/", "\\"]:
        direction = trav_floor.tileAt(*start).turns[direction]
    beams = [Beam(trav_floor, *start, direction)]
    visited: set[Tile] = set()
    visited_dir: set[tuple[str, Tile]] = set()
    while beams and len(visited) < trav_floor.size:
        beam = beams.pop(0)
        while not beam.done and (beam.direction, beam.current_tile) not in visited_dir:
            visited.add(beam.current_tile)
            visited_dir.add((beam.direction, beam.current_tile))
            beam.move()
        if beam.split == "horizontal":
            beams.extend(
                [
                    Beam(trav_floor, beam.x, beam.y, "left"),
                    Beam(trav_floor, beam.x, beam.y, "right"),
                ]
            )
        elif beam.split == "vertical":
            beams.extend(
                [
                    Beam(trav_floor, beam.x, beam.y, "up"),
                    Beam(trav_floor, beam.x, beam.y, "down"),
                ]
            )
    return trav_floor


if __name__ == "__main__":
    tiles_str = handle_input("puzzle input.txt")
    floor = Floor(tiles_str)
    energized_floor = traverse_floor(floor)
    print(f"Part 1: {len(energized_floor.get_energized())}")

    border_coords = floor.get_border()

    energized_opts = []
    for coords in border_coords:
        if "top" in floor.tileAt(*coords).grid_pos:
            energized_opts.append(traverse_floor(floor, coords, "down").get_energized())
        elif "bottom" in floor.tileAt(*coords).grid_pos:
            energized_opts.append(traverse_floor(floor, coords, "up").get_energized())
        # Separate if statements so that two beams are created for corner tiles
        if "left" in floor.tileAt(*coords).grid_pos:
            energized_opts.append(
                traverse_floor(floor, coords, "right").get_energized()
            )
        elif "right" in floor.tileAt(*coords).grid_pos:
            energized_opts.append(traverse_floor(floor, coords, "left").get_energized())

    # This takes about a minute to complete
    # TODO: implement a tiered caching mechanism
    print(f"Part 2: {max([len(opt) for opt in energized_opts])}")
