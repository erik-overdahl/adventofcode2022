#!/usr/bin/env python3

with open("./day7.input") as f:
    input = f.readlines()

stack = []
sizes = {}
for line in open("./day7.input"):
    tokens = line.rstrip("\n").split(" ")
    if tokens[0] == "$" and tokens[1] == "cd":
        dir = tokens[2]
        if dir == "..":
            stack.pop()
        else:
            stack.append(dir + "/")
    if tokens[0] != "dir" and tokens[0] != "$":
        size = int(tokens[0])
        n = ""
        for p in stack:
            n += p
            sizes[n] = sizes.get(n,0) + size


part1 = sum(filter(lambda x: x <= 100000, sizes.values()))
must_free = sizes["//"] - 40_000_000
part2 = min(filter(lambda x: x >= must_free , sizes.values()))

print(f"Part 1: {part1}, Part 2: {part2}")
