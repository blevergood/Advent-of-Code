#!/usr/bin/env python3
import sympy


class Trajectory:
    def __init__(self, pos: tuple[float], velocity: tuple[int]) -> None:
        self.pos = pos
        self.velocity = velocity

    def __str__(self) -> str:
        return f"pos: {self.pos}, velocity: {self.velocity}"

    def __repr__(self) -> str:
        return str(self)

    def get_pos_at_t(self, t: int) -> tuple[float, ...]:
        new_pos = []
        for axis, axis_val in enumerate(self.pos):
            print(axis)
            print(axis_val)
            new_pos.append(axis_val + t * self.velocity[axis])

        return tuple(new_pos)

    def get_y_slope(self) -> float:
        return self.velocity[1] / self.velocity[0]

    def get_y_intercept(self) -> float:
        return self.pos[1] - self.get_y_slope() * self.pos[0]

    # Currently only handles 2D
    def intersects_with(self, other: "Trajectory") -> tuple[float, ...]:
        if self.get_y_slope() == other.get_y_slope():
            return False
        x = (other.get_y_intercept() - self.get_y_intercept()) / (
            self.get_y_slope() - other.get_y_slope()
        )
        y = self.get_y_slope() * x + self.get_y_intercept()
        return (x, y)

    def get_time_at_pos(self, pos: tuple[float]) -> float:
        return (pos[0] - self.pos[0]) / self.velocity[0]


def handle_input(input: str) -> list[Trajectory]:
    f = open(input, "r")
    lines = f.read().split("\n")
    f.close()
    trajectories = []
    for line in lines:
        pos, velocity = line.split(" @ ")
        trajectories.append(
            Trajectory(
                tuple([float(coord) for coord in pos.split(", ")]),
                tuple([int(coord) for coord in velocity.split(", ")]),
            )
        )
    return trajectories


def in_bounds(pos: tuple[float, ...], area_min: int, area_max: int):
    for dim in pos:
        if dim < area_min or dim > area_max:
            return False
    return True


def get_pairs(trajectories: list[Trajectory]) -> list[tuple[Trajectory, Trajectory]]:
    return [
        (a, b) for idx, a in enumerate(trajectories) for b in trajectories[idx + 1 :]
    ]


def get_intersections(
    trajectories_pairs: list[Trajectory], area_min: int, area_max: int
) -> tuple[float, ...]:
    intersections = []
    for a, b in trajectories_pairs:
        intersection = a.intersects_with(b)
        if (
            intersection != False
            and a.get_time_at_pos(intersection) >= 0
            and b.get_time_at_pos(intersection) >= 0
            and in_bounds(intersection, area_min, area_max)
        ):
            intersections.append(intersection)
    return intersections


def hit_all_hail(trajectories: list[Trajectory]):
    x_r, y_r, z_r, vx_r, vy_r, vz_r = sympy.symbols("x_r, y_r, z_r, vx_r, vy_r, vz_r")
    equations = []
    for trajectory in trajectories[:10]:
        x_h, y_h, z_h = trajectory.pos
        vx_h, vy_h, vz_h = trajectory.velocity
        equations.append(
            sympy.Eq((x_r - x_h) * (vy_h - vy_r), (y_r - y_h) * (vx_h - vx_r))
        )
        equations.append(
            sympy.Eq((z_r - z_h) * (vx_h - vx_r), (x_r - x_h) * (vz_h - vz_r))
        )
    solutions = sympy.solve(equations, dict=True)
    return solutions[0]


if __name__ == "__main__":
    trajectories = handle_input("puzzle input.txt")
    pairs = get_pairs(trajectories)
    intersections = get_intersections(pairs, 200000000000000, 400000000000000)
    print(f"Part 1: {len(intersections)}")

    coeffs = hit_all_hail(trajectories)
    print(f"Part 2: {sum([coeffs[sympy.Symbol(c)] for c in ['x_r', 'y_r', 'z_r']])}")
