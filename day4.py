#!/usr/bin/env python3


def test_containment(x: list[int], y: list[int]) -> bool:
    return (x[0] <= y[0] and x[1] >= y[1]) or (x[0] >= y[0] and x[1] <= y[1])


def test_overlap(x: list[int], y: list[int]) -> bool:
    return (x[0] <= y[1] and y[0] <= x[1])


part1, part2 = 0, 0
with open("./day4.input") as f:
    for line in f:
        elves = line.rstrip("\n").split(",")
        s = list(map(lambda x: list(map(int, x.split("-"))), elves))
        if test_containment(*s):
            part1 += 1
        if test_overlap(*s):
            part2 += 1

print(f"Part 1: {part1}, Part 2: {part2}")
