#!/usr/bin/env python3

def print_board(rows: list[int]):
    print()
    for r in rows[::-1]:
        print(f"{r:08b}".replace("0",".").replace("1","#"))


def print_rock(rock: int):
    for i in range(4):
        print(f"{(rock >> (4-i)*8) & 0xFF:08b}".replace("0",".").replace("1","#"))


def shift(direction: str, rock:int, row_mask: int) -> int:
    s = rock >> 1 if direction == ">" else rock << 1
    if not s & row_mask:
        return s
    return rock


def drop_rocks(count: int, jets: str) -> int:
    rocks = [
        # 00000000
        # 00000000
        # 00000000
        # 00111100
        int.from_bytes([0x00,0x00,0x00,0x3C]),
        # 00000000
        # 00010000
        # 00111000
        # 00010000
        int.from_bytes([0x00,0x10,0x38,0x10]),
        # 00000000
        # 00001000
        # 00001000
        # 00111000
        int.from_bytes([0x00,0x08,0x08,0x38]),
        # 00100000
        # 00100000
        # 00100000
        # 00100000
        int.from_bytes([0x20,0x20,0x20,0x20]),
        # 00000000
        # 00000000
        # 00110000
        # 00110000
        int.from_bytes([0x00,0x00,0x30,0x30]),
    ]
    rows = []
    # sometimes I hate pyright
    seen: list[tuple[int,int]] = [(0,0) for _ in range(len(rocks)*len(jets))]
    last_jet = len(jets) - 1
    jet = 0
    pos = 0
    top = 0

    for r in range(count):
        i = r % 5
        rock = rocks[i]
        sig = jet*5 + i
        # if we have seen this rock/specific jet combo before, and the
        # number of rocks dropped between then and now fits evenly into
        # the number of rocks we have remaining
        if seen[sig] != (0,0):
            cycle_start, prev_top = seen[sig]
            cycle_len = r - cycle_start
            repeats, offset = divmod(count - r, cycle_len)
            if offset == 0:
                return top + (top - prev_top)*repeats
        seen[sig] = (r, top)

        # every dropped rock gets 3 shifts
        row_mask = 0x01_01_01_01
        rock = shift(jets[jet], rock, row_mask)
        jet = jet + 1 if jet < last_jet else 0
        rock = shift(jets[jet], rock, row_mask)
        jet = jet + 1 if jet < last_jet else 0
        rock = shift(jets[jet], rock, row_mask)
        jet = jet + 1 if jet < last_jet else 0

        while True:
            # shift if not blocked
            rock = shift(jets[jet], rock, row_mask)
            jet = jet + 1 if jet < last_jet else 0

            if pos == 0 or (rock & ((row_mask << 8) | rows[pos - 1])):
                break
            pos -= 1
            row_mask = (row_mask << 8) | rows[pos]

        for i in range(4):
            row = pos + i
            val = rock & 0xFF
            if val == 0:
                break
            if row < len(rows):
                rows[row] |= val
            else:
                rows.append(val | 1)
            for c in range(1,8):
                if rows[row] & (1 << c):
                    top = max(row+1, top)
            rock >>= 8

        pos = len(rows)
    return top


jets = open("./day17.input").read().rstrip("\n")
# jets = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

part1 = drop_rocks(2022,jets)
part2 = drop_rocks(int(1e12),jets)
print(f"Part 1: {part1}, Part 2: {part2}")
