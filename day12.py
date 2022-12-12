#!/usr/bin/env python3

from dataclasses import dataclass, field
from collections import deque
from typing import Callable

@dataclass
class Node:
    value: int
    neighbors: list[int] = field(default_factory=list)


@dataclass
class Graph:
    start: int
    end: int
    nodes: list[Node]


def parse_graph(input: str) -> Graph:
    lines = input.split("\n")
    col_len, line_len = len(lines), len(lines[0])
    nodes = []
    start, end = 0,0
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            v = ord(char)
            if char == "S":
                v = ord("a")
                start = (y*line_len) + x
            elif char == "E":
                v = ord('z')
                end = (y*line_len) + x
            neighbors = []
            if y > 0:
                neighbors.append(((y - 1)*line_len) + x)
            if y < (col_len - 1):
                neighbors.append(((y + 1)*line_len) + x)
            if x > 0:
                neighbors.append((y*line_len) + x - 1)
            if x < (line_len - 1):
                neighbors.append((y*line_len) + x + 1)
            n = Node(v, neighbors)
            nodes.append(n)
    return Graph(start, end, nodes)


def BFS(graph: Graph, traversable: Callable[[Node,Node],bool], exit_condition: Callable[[int,int],bool]) -> tuple[int, list[int]]:
    discovered = [False for _ in graph.nodes]
    # processed = [False for _ in graph.nodes]
    parents = [-1 for _ in graph.nodes]

    queue = deque()
    queue.append(graph.start)
    discovered[graph.start] = True

    while len(queue) > 0:
        index = queue.popleft()
        # processed[index] = True
        node = graph.nodes[index]
        for n_idx in node.neighbors:
            if not discovered[n_idx]:
                neighbor = graph.nodes[n_idx]
                if traversable(node, neighbor):
                    discovered[n_idx] = True
                    parents[n_idx] = index
                    queue.append(n_idx)
                    if exit_condition(n_idx, neighbor.value):
                        return n_idx, parents
                    # print_path(parents)
    return 0, parents


def can_move_uphill(node: Node, neighbor: Node) -> bool:
    return (node.value + 1) >= neighbor.value


def can_move_downhill(node: Node, neighbor: Node) -> bool:
    return (node.value - 1) <= neighbor.value


def path_len(parents: list[int], start: int, target: int) -> int:
    path_len = 1
    next = parents[start]
    while next != target:
        next = parents[next]
        path_len += 1
    return path_len


input = open("./day12.input").read().strip("\n")

graph = parse_graph(input)

_, parents = BFS(graph,
                 can_move_uphill,
                 lambda n_idx, _: n_idx == graph.end)
part1 = path_len(parents, graph.end, graph.start)

graph.start = graph.end
end_pos, parents = BFS(graph,
                       can_move_downhill,
                       lambda _, val: val == ord('a'))
part2 = path_len(parents, end_pos, graph.start)

print(f"Part 1: {part1}, Part 2: {part2}")
