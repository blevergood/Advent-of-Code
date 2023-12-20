#!/usr/bin/env python3
class Tile:
    def __init__(
        self, value: str, x: int, y: int, grid_pos: str, energized=False
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
                if i == 0 and j == 0:
                    energized = True
                else:
                    energized = False
                current_row.append(
                    Tile(tiles_str[i][j], j, i, y_pos + x_pos, energized)
                )
            self.tiles.append(current_row)

    def tileAt(self, x, y):
        return self.tiles[y][x]

    def get_energized(self):
        energized_tiles = []
        for row in self.tiles:
            for tile in row:
                if tile.energized:
                    energized_tiles.append(tile)
        return energized_tiles


class Light:
    def __init__(self, floor: Floor, x: int, y: int, direction: str) -> None:
        self.x = x
        self.y = y
        self.floor = floor
        self.direction = direction
        self.current_tile = self.floor.tileAt(self.x, self.y)
        self.current_tile.energized = True
        self.done = False
        self.split = ""

    def move_right(self):
        if "right" not in self.current_tile.grid_pos:
            self.x += 1

    def move_left(self):
        if "left" not in self.current_tile.grid_pos:
            self.x -= 1

    def move_up(self):
        if "top" not in self.current_tile.grid_pos:
            self.y -= 1

    def move_down(self):
        if "bottom" not in self.current_tile.grid_pos:
            self.y += 1

    def move(self):
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


def traverse_floor(floor):
    # Need to account for if the first tile itself is a mirror
    if floor.tileAt(0, 0).value in ["/", "\\"]:
        direction = floor.tileAt(0, 0).turns["right"]
    elif floor[0][0].value == "|":
        direction = "down"
    beams = [Light(floor, 0, 0, direction)]
    visited: set[Tile] = set()
    visited_dir: set[tuple[str, Tile]] = set()
    while beams and len(visited) < floor.size:
        beam = beams.pop(0)
        while not beam.done and (beam.direction, beam.current_tile) not in visited_dir:
            visited.add(beam.current_tile)
            visited_dir.add((beam.direction, beam.current_tile))
            beam.move()
        if beam.split == "horizontal":
            beams.extend(
                [
                    Light(floor, beam.x, beam.y, "left"),
                    Light(floor, beam.x, beam.y, "right"),
                ]
            )
        elif beam.split == "vertical":
            beams.extend(
                [
                    Light(floor, beam.x, beam.y, "up"),
                    Light(floor, beam.x, beam.y, "down"),
                ]
            )
    return floor


if __name__ == "__main__":
    tiles_str = handle_input("puzzle input.txt")
    floor = Floor(tiles_str)
    energized_floor = traverse_floor(floor)
    print(f"Part 1: {len(energized_floor.get_energized())}")
