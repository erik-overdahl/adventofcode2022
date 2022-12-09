#!/usr/bin/env python3

def head_positions(input: list[str]) -> list[tuple[int,int]]:
    x,y = 0,0
    moves: list[tuple[int,int]] = [(x,y)]
    for line in input:
        dir, steps = line.split(" ")
        for _ in range(int(steps)):
            match dir:
                case "R":
                    x += 1
                case "L":
                    x -= 1
                case "U":
                    y += 1
                case "D":
                    y -= 1
            moves.append((x,y))
    return moves


def nth_knot_positions(moves: list[tuple[int,int]], n:int=1) -> list[tuple[int,int]]:
    if n == 0:
        return moves
    x, y = 0, 0
    positions: list[tuple[int,int]] = [(x,y)]
    for head in moves:
        if abs(head[0] - x) > 1 or abs(head[1] - y) > 1:
            x += (head[0] > x) - (head[0] < x)
            y += (head[1] > y) - (head[1] < y)
        positions.append((x,y))
    return nth_knot_positions(positions, n-1)


input = open("./day9.input").readlines()
moves = head_positions(input)
part1 = nth_knot_positions(moves)
part2 = nth_knot_positions(moves, 9)
print(f"Part 1: {len(set(part1))}, Part 2: {len(set(part2))}")
