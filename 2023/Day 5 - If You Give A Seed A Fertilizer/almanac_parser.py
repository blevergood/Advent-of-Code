#!/usr/bin/env python3
import re


class AlmanacRange:
    def __init__(self, start: int, length: int) -> None:
        self.start = start
        self.end = start + length

    def contains(self, value: int) -> bool:
        if value < self.start:
            return False
        elif value > self.end:
            return False
        else:
            return True


class AlmanacMap:
    def __init__(self, ranges: list[list[int]]) -> None:
        self.mapping = dict()
        for r in ranges:
            dest_start, src_start, length = r
            self.mapping[AlmanacRange(src_start, length)] = AlmanacRange(
                dest_start, length
            )

    def mapped_number(self, source: int) -> int:
        for k in self.mapping.keys():
            if k.contains(source):
                return self.mapping[k].start + (source - k.start)
        return source


def get_closest_location(source: str) -> int:
    f = open(source, "r")
    segments = f.read().split("\n\n")

    seeds = [int(match) for match in re.findall(r"\d+", segments.pop(0))]

    (
        seed_soil,
        soil_fertilizer,
        fertilizer_water,
        water_light,
        light_temp,
        temp_humid,
        humid_location,
    ) = [
        AlmanacMap(
            [
                [int(match) for match in re.findall(r"\d+", map)]
                for map in segment.split("\n")[1:]
            ]
        )
        for segment in segments
    ]

    locations = [
        humid_location.mapped_number(
            temp_humid.mapped_number(
                light_temp.mapped_number(
                    water_light.mapped_number(
                        fertilizer_water.mapped_number(
                            soil_fertilizer.mapped_number(seed_soil.mapped_number(seed))
                        )
                    )
                )
            )
        )
        for seed in seeds
    ]

    f.close()
    return min(locations)


if __name__ == "__main__":
    print("Part 1:", get_closest_location("./puzzle input.txt"))
