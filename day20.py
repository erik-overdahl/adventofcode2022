#!/usr/bin/env python3

class Node:
    def __init__(self, value: int, next: "Node", prev: "Node"):
        self.value = value
        self.next = next
        self.prev = prev


def parse_list(input: str, key: int = 1) -> list[Node]:
    nodes = []
    prev = None
    for n in input.split("\n"):
        node = Node(int(n)*key, None, prev)
        nodes.append(node)
        prev = node
    nodes[0].prev = prev
    m = len(nodes)
    for i, node in enumerate(nodes):
        node.next = nodes[(i+1) % m]
    return nodes


def print_list(l: list[Node]):
    values = []
    n = l[0]
    for _ in range(len(l)):
        values.append(n.value)
        n = n.next
    print(values)


def decrypt(l: list[Node]) -> Node:
    m = len(l) - 1
    head = l[0]
    for node in l:
        if node.value == 0:
            head = node
        # print_list(l)
        prev = node.prev
        next = node.next
        node.next.prev = prev
        node.prev.next = next

        steps = node.value % m
        for _ in range(steps):
            prev = prev.next
            next = next.next

        prev.next = node
        node.prev = prev
        next.prev = node
        node.next = next
    # print_list(l)
    return head


def grove_coordinates(head: Node, length: int) -> list[int]:
    n = head
    coord_positions = sorted([x%length for x in (1000,2000,3000)])
    grove_coords = [0,0,0]
    i = 0
    for coord, pos in enumerate(coord_positions):
        while i < pos:
            n = n.next
            i += 1
        grove_coords[coord] = n.value
    return grove_coords



input = open("./day20.input").read().rstrip("\n")
# input = """1\n2\n-3\n3\n-2\n0\n4"""

l = parse_list(input)
head = decrypt(l)
coords = grove_coordinates(head, len(l))
part_1 = sum(coords)

nodes = parse_list(input, 811589153)
head = None
for _ in range(10):
    head = decrypt(nodes)

coords = grove_coordinates(head, len(nodes))
part_2 = sum(coords)

print(f"Part 1: {part_1}, Part 2: {part_2}")
