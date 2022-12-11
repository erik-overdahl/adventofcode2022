#!/usr/bin/env python3

import operator
from typing import Callable

class Monkey:
    def __init__(self, op: Callable[[int],int], test: int, neighbors: tuple[int,int], initial_items: list[int] = []):
        self.op = op
        self.test = test
        self.neighbors = neighbors
        self.items = initial_items
        self.seen = 0

    def inspect(self, item: int) -> int:
        return self.op(item)

    def next(self, item: int) -> int:
        return self.neighbors[(item % self.test) > 0]


def parse_monkey(input: list[str]) -> Monkey:
    items = [int(i) for i in input[1].split(":")[1].split(",")]
    op_line = input[2].split(" ")
    arg = op_line[-1]
    op = operator.add # sensible default?
    if arg == "old":
        op = operator.pow
    elif op_line[-2] == "*":
        op = operator.mul
    a = 2 if arg == "old" else int(arg)
    f = lambda x,const=a: op(x, const)
    test = int(input[3].split(" ")[-1])
    neighbors = (int(input[4].split(" ")[-1]), int(input[5].split(" ")[-1]))
    return Monkey(f, test, neighbors, items)


def business_level(monkeys: list[Monkey]) -> int:
    busiest = [0,0]
    for m in monkeys:
        if m.seen > busiest[0]:
            busiest = [m.seen, busiest[0]]
        elif m.seen > busiest[1]:
            busiest[1] = m.seen
    return busiest[0] * busiest[1]


def simulate(monkeys: list[Monkey], rounds: int, adjust: Callable[[int], int]) -> int:
    for round in range(rounds):
        for m in monkeys:
            for item in m.items:
                new = adjust(m.inspect(item))
                monkeys[m.next(new)].items.append(new)
            m.seen += len(m.items)
            m.items = []

    return business_level(monkeys)


input = open("./day11.input").read()

monkeys = [parse_monkey(desc.split("\n")) for desc in input.split("\n\n")]
part1 = simulate(monkeys, 20, lambda worry: worry // 3)

monkeys = [parse_monkey(desc.split("\n")) for desc in input.split("\n\n")]
lcm = 1
for m in monkeys:
    lcm *= m.test

part2 = simulate(monkeys, 10000, lambda worry: worry % lcm)

print(f"Part 1: {part1}, Part 2: {part2}")
