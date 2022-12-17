#!/usr/bin/env python3

from collections import deque

class Valve:
    def __init__(self, name: str, rate: int):
        self.name = name
        self.flow = rate
        self.edges: list[tuple[int,"Valve"]] = []

    def __repr__(self):
        return f"Valve({self.name}, {self.flow})"


def parse_graph(input: str) -> list[Valve]:
    valves = {}
    lines = [line.split(" ") for line in input.split("\n")]
    for tokens in lines:
        name = tokens[1]
        rate = int(tokens[4][5:-1])
        valves[name] = Valve(name, rate)
    for tokens in lines:
        name = tokens[1]
        valve = valves[name]
        for s in tokens[9:]:
            neighbor = valves[s.rstrip(",")]
            valve.edges.append((1, neighbor))
    return list(valves.values())


def reduce_graph(graph: list[Valve]) -> list[Valve]:
    reduced = []
    for v in graph:
        seen = set()
        seen.add(v)
        if v.flow == 0 and v.name != "AA":
            continue
        neighbors = []
        queue = deque(v.edges)
        while len(queue) > 0:
            dist, neighbor = queue.popleft()
            seen.add(neighbor)
            if neighbor.name == "AA":
                neighbors.append((dist, neighbor))
            if neighbor.flow > 0:
                neighbors.append((dist, neighbor))
            else:
                for d, n in neighbor.edges:
                    if n not in seen:
                        queue.append((dist + d, n))
        v.edges = neighbors
        reduced.append(v)
    reduced.sort(key=lambda v: v.name)
    return reduced


def adjacency_matrix(graph: list[Valve]) -> list[list[int]]:
    indices = {v.name:i for i, v in enumerate(graph)}
    matrix = [[10000 for _ in graph] for _ in graph]
    for i, valve in enumerate(graph):
        row = matrix[i]
        row[i] = 0
        for dist, neighbor in valve.edges:
            n_idx = indices[neighbor.name]
            row[n_idx] = dist
    return matrix


# Ford-Warshall algorithm
def shortest_paths(edges: list[list[int]]) -> list[list[int]]:
    edges = [[dist for dist in row] for row in edges]
    for k in range(len(edges)):
        for i in range(len(edges)):
            for j in range(len(edges)):
                edges[i][j] = min(edges[i][j], edges[i][k] + edges[k][j])
    return edges


def graph_to_dot(valves: list[Valve]):
    valves.sort(key=lambda v: v.name)
    seen = set()
    s = ["graph {"]
    for v in valves:
        seen.add(v)
        s.append(f"\t{v.name} [label=\"{v.name}\\n{v.flow}\"]")
        for dist, n in v.edges:
            if n not in seen:
                s.append(f"\t{ v.name } -- {n.name} [label={dist}];")
    s.append("}")
    content = "\n".join(s)
    with open("./day16.dot", "w") as f:
        f.write(content)


class Solver:
    def __init__(self, graph: list[Valve]):
        self.graph = graph
        self.distances: list[list[int]] = shortest_paths(adjacency_matrix(graph))
        self.cache = {}
        self.all_open = 2**len(graph) - 1
        self.flow_cache = {self.all_open:sum([v.flow for v in graph])}


    def flow_rate(self, open_valves: int) -> int:
        if open_valves not in self.flow_cache:
            self.flow_cache[open_valves] = sum([v.flow for i, v in enumerate(self.graph) if open_valves & (1 << i)])
        return self.flow_cache[open_valves]


    def max_pressure_release(self, time: int, node: int = 0, open_valves: int = 1) -> int:
        # print(f"At {self.graph[node].name} with {time} minutes and {bin(open_valves)} open")
        state = (time,node,open_valves)
        if state in self.cache:
            return self.cache[state]
        current_flow = self.flow_rate(open_valves)
        if time == 1 or open_valves == self.all_open:
            self.cache[state] = current_flow * time
            return self.cache[state]

        max_flows = [current_flow * time]
        valve_open = open_valves & (1 << node)
        if not valve_open:
            max_flows.append(current_flow + self.max_pressure_release(time - 1, node, open_valves | (1 << node)))
        neighbors = [(i, dist) for i, dist in enumerate(self.distances[node]) if dist < time and i != node]
        for i, dist in neighbors:
            max_flows.append((current_flow * dist) + self.max_pressure_release(time - dist, i, open_valves))
        self.cache[state] = max(max_flows)
        return self.cache[state]


input = open("./day16.input").read().rstrip("\n")
# input = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
# Valve BB has flow rate=13; tunnels lead to valves CC, AA
# Valve CC has flow rate=2; tunnels lead to valves DD, BB
# Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
# Valve EE has flow rate=3; tunnels lead to valves FF, DD
# Valve FF has flow rate=0; tunnels lead to valves EE, GG
# Valve GG has flow rate=0; tunnels lead to valves FF, HH
# Valve HH has flow rate=22; tunnel leads to valve GG
# Valve II has flow rate=0; tunnels lead to valves AA, JJ
# Valve JJ has flow rate=21; tunnel leads to valve II"""


graph = reduce_graph(parse_graph(input))
solver = Solver(graph)
print(solver.max_pressure_release(30))
