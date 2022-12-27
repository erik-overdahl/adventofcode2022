#!/usr/bin/env python3


def parse_elves(input: str) -> set[complex]:
    elves = set()
    for y, line in enumerate(input.rstrip("\n").split("\n")):
        for x, c in enumerate(line):
            if c == "#":
                elves.add(complex(y,x))
    return elves


def print_elves(elves: set[complex]):
    minY, maxY, minX, maxX = 10000, 0, 10000, 0
    for e in elves:
        y, x = e.real, e.imag
        if y < minY:
            minY = y
        elif y > maxY:
            maxY = y
        if x < minX:
            minX = x
        elif x > maxX:
            maxX = x
    shift = complex(minY, minX)
    size = complex(maxY, maxX) - shift
    board = [["." for _ in range(int(size.imag + 1))] for _ in range(int(size.real + 1))]
    for e in elves:
        p = e - shift
        y, x = int(p.real), int(p.imag)
        board[y][x] = "#"
    print('\n'.join([''.join(l) for l in board]))


def propose(e: complex, occupied: list[bool], d: int) -> complex:
    if any(occupied):
        neighborhoods = [
            occupied[0:3], # N
            occupied[4:7], # S
            occupied[2:5], # W
            occupied[6:] + occupied[0:1] # E
        ]
        moves = [-1, 1, 0 - 1j, 0 + 1j]
        for i in range(4):
            if not any(neighborhoods[(d+i) % 4]):
                return e + moves[(d+i) % 4]
    return e




def round(elves: set[complex], d: int) -> set[complex]:
    proposed = {}
    next = set()
    for e in elves:
        neighbors = [e + p for p in
                     [
                         -1 + 1j, # 0 NE
                         -1,      # 1 N
                         -1 - 1j, # 2 NW
                         0 - 1j,  # 3 W
                         1 - 1j,  # 4 SW
                         1,       # 5 S
                         1 + 1j,  # 6 SE
                         0 + 1j   # 7 E
                     ]]
        occupied = [n in elves for n in neighbors]
        move = propose(e, occupied, d)
        if move != e:
            proposers = proposed.get(move, [])
            proposers.append(e)
            proposed[move] = proposers
        else:
            next.add(e)
    for spot, proposers in proposed.items():
        if len(proposers) == 1:
            next.add(spot)
        else:
            for e in proposers:
                next.add(e)
    return next


def non_elf_spaces(elves: set[complex]) -> int:
    minY, maxY, minX, maxX = 10000, 0, 10000, 0
    for e in elves:
        y, x = e.real, e.imag
        if y < minY:
            minY = y
        elif y > maxY:
            maxY = y
        if x < minX:
            minX = x
        elif x > maxX:
            maxX = x

    return int((maxY - minY + 1) * (maxX - minX + 1) - len(elves))


input = open("./day23.input").read().rstrip("\n")

part_1 = -1

elves = parse_elves(input)
next = round(elves, 0)
i = 1
while next != elves:
    elves = next
    if i == 10:
        part_1 = non_elf_spaces(elves)
    next = round(elves, i)
    i += 1

part_2 = i

print(f"Part 1: {part_1}, Part 2: {part_2}")
