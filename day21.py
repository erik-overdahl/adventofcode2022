#!/usr/bin/env python3

from abc import abstractmethod, ABC
from operator import add, sub, mul, ifloordiv as div
from typing import Callable

CACHE_HITS = 0

class Monkey(ABC):
    @abstractmethod
    def value(self) -> int:
        pass


class NumMonkey(Monkey):
    def __init__(self, val: int):
        self.val = val

    def value(self) -> int:
        return self.val


class OpMonkey(Monkey):
    def __init__(self, left: Monkey, right: Monkey, op: Callable[[int,int],int]):
        self.left = left
        self.right = right
        self.op = op
        self.val = None

    def value(self) -> int:
        return self.op(self.left.value(), self.right.value())


input = open("./day21.input").read()
# input = """
# root: pppw + sjmn
# dbpl: 5
# cczh: sllz + lgvd
# zczc: 2
# ptdq: humn - dvpt
# dvpt: 3
# lfqf: 4
# humn: 5
# ljgn: 2
# sjmn: drzm * dbpl
# sllz: 4
# pppw: cczh / lfqf
# lgvd: ljgn * ptdq
# drzm: hmdt - zczc
# hmdt: 32
# """

monkeys = {}
op_friends = {}
parents = {}
for line in input.strip("\n").split("\n"):
    name = line[0:4]
    try:
        if line[6].isnumeric():
            monkeys[name] = NumMonkey(int(line[6:]))
        else:
            op = add
            if line[11] == "*":
                op = mul
            elif line[11] == "-":
                op = sub
            elif line[11] == "/":
                op = div
            monkeys[name] = OpMonkey(None, None, op)
            friends = line[6:].split(" ")
            op_friends[name] = friends
            parents[friends[0]] = name
            parents[friends[2]] = name
    except:
        print(line)

for name, friends in op_friends.items():
    m = monkeys[name]
    m.left = monkeys[friends[0]]
    m.right = monkeys[friends[2]]

root = monkeys["root"]
part_1 = root.value()

path = [monkeys["humn"]]
p = parents["humn"]
while p != "root":
    path.append(monkeys[p])
    p = parents[p]

l_ops = {
    add: sub,
    sub: add,
    mul: div,
    div: mul,
}
r_ops = {
    add: sub,
    sub: lambda v,l: l - v,
    mul: div,
    div: lambda v,l: l//v,
}

human = monkeys["humn"]

n = root
var = path.pop()
val = n.left if var == n.right else n.right
part_2 = val.value()
while len(path) > 0:
    n = var
    var = path.pop()
    if var == n.left:
        val = n.right.value()
        op = l_ops[n.op]
    else:
        val = n.left.value()
        op = r_ops[n.op]
    part_2 = op(part_2, val)

human.val = part_2
assert root.left.value() == root.right.value()

print(f"Part 1: {part_1}, Part 2: {part_2}")
