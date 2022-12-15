#!/usr/bin/env python3

from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Line:
    left: int
    right: int

@dataclass
class Area:
    sensor: complex
    beacon: complex
    manhattan: int = field(init=False)
    upper: int = field(init=False)
    lower: int = field(init=False)
    left: int = field(init=False)
    right: int = field(init=False)

    def __post_init__(self):
        self.manhattan = int(abs(self.sensor.real - self.beacon.real) + abs(self.sensor.imag - self.beacon.imag))
        self.lower = int(self.sensor.imag - self.manhattan)
        self.upper = int(self.sensor.imag + self.manhattan)
        self.left = int(self.sensor.real - self.manhattan)
        self.right = int(self.sensor.real + self.manhattan)

    def segment_at_y(self, y: int, bound: Optional[Line]) -> Line:
        x_dist = abs(self.sensor.imag - self.lower) - abs(self.sensor.imag - y)
        if bound:
            return Line(
                max(bound.left, int(self.sensor.real - x_dist)),
                min(bound.right, int(self.sensor.real + x_dist)))
        else:
            return Line(int(self.sensor.real - x_dist), int(self.sensor.real + x_dist))


def parse_points(input: str) -> list[Area]:
    areas = []
    for line in input.split("\n"):
        pieces = line.split(": ")
        t = pieces[0].split(" ")
        sensor = complex(int(t[-2][2:-1]), int(t[-1][2:]))
        t = pieces[1].split(" ")
        beacon = complex(int(t[-2][2:-1]), int(t[-1][2:]))
        areas.append(Area(sensor, beacon))
    return areas


def segments_at_y(areas: list[Area], y: int, bound: Optional[Line]) -> list[Line]:
    if bound:
        segs = [area.segment_at_y(y, bound) for area in areas if area.lower <= y <= area.upper and area.right > bound.left and area.left < bound.right]
    else:
        segs = [area.segment_at_y(y, None) for area in areas if area.lower <= y <= area.upper]
    return sorted(
        segs,
        key=lambda s: s.left
    )

def combine_segments(segments: list[Line]) -> list[Line]:
    result = []
    left, right = segments[0].left, segments[0].right
    for s in segments[1:]:
        if s.left > right:
            result.append(Line(left, right))
            left = s.left
        if s.right > right:
            right = s.right
    result.append(Line(left, right))
    return result


def coverage_at_y(areas: list[Area], y: int) -> int:
    segments = combine_segments(segments_at_y(areas, y, None))
    num_points = 0
    for s in segments:
        num_points += abs(s.right - s.left)
    return num_points


def find_distress(areas: list[Area], bound: Line) -> complex:
    for y in range(bound.left, bound.right+1):
        x = 0
        segments = combine_segments(segments_at_y(areas, y, bound))
        for s in segments:
            if s.left <= x:
                x = s.right + 1
            else:
                return complex(x, y)
            if x > bound.right:
                break
    return complex(0,0)


def tuning_freq(beacon: complex) -> int:
    return int((4000000*beacon.real) + beacon.imag)


input = open("./day15.input").read().rstrip("\n")
# input = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
# Sensor at x=9, y=16: closest beacon is at x=10, y=16
# Sensor at x=13, y=2: closest beacon is at x=15, y=3
# Sensor at x=12, y=14: closest beacon is at x=10, y=16
# Sensor at x=10, y=20: closest beacon is at x=10, y=16
# Sensor at x=14, y=17: closest beacon is at x=10, y=16
# Sensor at x=8, y=7: closest beacon is at x=2, y=10
# Sensor at x=2, y=0: closest beacon is at x=2, y=10
# Sensor at x=0, y=11: closest beacon is at x=2, y=10
# Sensor at x=20, y=14: closest beacon is at x=25, y=17
# Sensor at x=17, y=20: closest beacon is at x=21, y=22
# Sensor at x=16, y=7: closest beacon is at x=15, y=3
# Sensor at x=14, y=3: closest beacon is at x=15, y=3
# Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

areas = parse_points(input)
part1 = coverage_at_y(areas, 2_000_000)
bound = Line(0,4_000_000)
part2 = tuning_freq(find_distress(areas, bound))

print(f"Part 1: {part1}, Part 2: {part2}")
