#!/usr/bin/env python3

from functools import reduce

def to_bitfield(string: str) -> int:
    field = 0
    for c in string:
        # a -> 1, A -> 27
        field |= 1 << (ord(c) - (38 if c.isupper() else 96))
    return field


def priority(bitfield: int) -> int:
    for j in range(53):
        if bitfield & (1 << j):
            return j
    return 0


with open("./day3.input") as f:
    lines = [line.rstrip("\n") for line in f]


tot_priority = sum(map(lambda x: priority(to_bitfield(x[:len(x)//2]) & to_bitfield(x[len(x)//2:])), lines))

group_priority = 0
for i in range(0, len(lines), 3):
    group_priority += priority(reduce(lambda x,y: x & y, map(to_bitfield, lines[i:i+3])))


print(f"Part 1: {tot_priority}, Part 2: {group_priority}")
