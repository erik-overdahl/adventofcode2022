#!/usr/bin/env python3

from collections import namedtuple

Point = namedtuple("Point", "x y")

def parse_lines(input: str) -> tuple[set[Point], int]:
    lowest = 0
    points = set()
    for line in input.rstrip("\n").split("\n"):
        coords = line.split(" -> ")
        p = [int(c) for c in coords[0].split(",")]
        for point in coords[1:]:
            next = [int(c) for c in point.split(",")]
            if p[0] == next[0]:
                x = p[0]
                for y in range(min(p[1],next[1]), max(p[1],next[1])+1):
                    lowest = max(y, lowest)
                    points.add(Point(x,y))
            else:
                y = p[1]
                lowest = max(y, lowest)
                for x in range(min(p[0],next[0]), max(p[0],next[0])+1):
                    points.add(Point(x,y))
            p = next
    return points, lowest


input = open("./day14.input").read()

# input = """498,4 -> 498,6 -> 496,6
# 503,4 -> 502,4 -> 502,9 -> 494,9
# """

part1 = 0

occupied, max_y = parse_lines(input)
num_rocks = len(occupied)
max_y += 2

start = Point(500,-1)
falling_path = []
while Point(500,0) not in occupied:
    grain = start
    falling = True
    while falling:
        falling_path.append(grain)
        falling = False
        for dx in [0, -1, 1]:
            next = Point(grain.x+dx, grain.y + 1)
            if next not in occupied and next.y < max_y:
                grain = next
                falling = True
                break
    if not part1 and grain.y == max_y-1:
        part1 = len(occupied) - num_rocks
    grain = falling_path.pop()
    occupied.add(grain)
    start = falling_path.pop()

part2 = len(occupied) - num_rocks

print(f"Part 1: {part1}, Part 2: {part2}")
