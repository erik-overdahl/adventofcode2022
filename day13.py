#!/usr/bin/env python3

from functools import cmp_to_key

Nest = int|list["Nest"]

def parse_list(line: str) -> Nest:
    current = []
    stack = []
    num = ""
    for char in line:
        match char:
            case "[":
                new = []
                current.append(new)
                stack.append(current)
                current = new
            case ",":
                if num != "":
                    current.append(int(num))
                    num = ""
            case "]":
                if num != "":
                    current.append(int(num))
                    num = ""
                current = stack.pop()
            case _:
                num += char
    return current[0]


def compare(left: Nest, right: Nest) -> int:
    match left, right:
        case int(), int():
            return left - right
        case list(), int():
            return compare(left, [right])
        case int(), list():
            return compare([left], right)
        case list(), list():
            for x in map(compare, left, right):
                if x: return x
            return compare(len(left), len(right))
    return 0


input = open("./day13.input").read()

pairs = [[parse_list(l) for l in p.split("\n")[:2]] for p in input.split("\n\n")]

part1 = sum(i for i,p in enumerate(pairs,1) if compare(*p) < 0)

packets = []
for p in pairs:
    packets.append(p[0])
    packets.append(p[1])

packets.append([[2]])
packets.append([[6]])

packets.sort(key=cmp_to_key(compare))

part2 = 1
for i, packet in enumerate(packets, 1):
    if packet in [[[2]], [[6]]]:
        part2 *= i

print(f"Part 1: {part1}, Part 2: {part2}")
