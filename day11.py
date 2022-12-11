#!/usr/bin/env python3

import operator
from typing import Callable

class Monkey:
    def __init__(self, op: Callable[[int],int], test: int, neighbors: tuple[int,int], initial_items: list[int] = []):
        self.op = op
        self.test = test
        self.neighbors = neighbors
        self.items = initial_items
        self.ptr = 0

    def inspect(self, item: int) -> int:
        return self.op(item)

    def next(self, item: int) -> int:
        return self.neighbors[(item % self.test) > 0]


def parse_monkey(input: list[str]) -> Monkey:
    items = [int(i) for i in input[1].split(":")[1].split(",")]
    op_line = input[2].split(" ")
    arg = op_line[-1]
    op = operator.add # sensible default?
    match op_line[-2]:
        case "+":
            op = operator.add
        case "-":
            op = operator.sub
        case "*":
            op = operator.mul
        case "/":
            op = operator.floordiv
    f = lambda x: op(x, x if arg == "old" else int(arg))
    test = int(input[3].split(" ")[-1])
    neighbors = (int(input[4].split(" ")[-1]), int(input[5].split(" ")[-1]))
    return Monkey(f, test, neighbors, items)


def business_level(monkeys: list[Monkey]) -> int:
    busiest = [0,0]
    for m in monkeys:
        if m.ptr > busiest[0]:
            busiest = [m.ptr, busiest[0]]
        elif m.ptr > busiest[1]:
            busiest[1] = m.ptr
    return busiest[0] * busiest[1]


def simulate(input: str, rounds: int, worry_divisor: int) -> int:
    monkeys = []
    for monkey_desc in input.split("\n\n"):
        monkeys.append(parse_monkey(monkey_desc.split("\n")))

    for round in range(rounds):
        for m in monkeys:
            start = m.ptr
            for item in m.items[start:]:
                new = m.inspect(item) // worry_divisor
                monkeys[m.next(new)].items.append(new)
            m.ptr = len(m.items)

    return business_level(monkeys)



input = open("./day11.input").read()

input = """ Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

part1 = simulate(input, 20, 3)
part2 = -1
# part2 = simulate(input, 10000, 1)
print(f"Part 1: {part1}, Part 2: {part2}")
