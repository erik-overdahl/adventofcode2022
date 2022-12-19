#!/usr/bin/env python3

def print_board(rows: list[int]):
    print()
    for r in rows[::-1]:
        print(f"{r:08b}".replace("0",".").replace("1","#"))


def print_rock(rock: int):
    for i in range(4):
        print(f"{(rock >> (4-i)*8) & 0xFF:08b}".replace("0",".").replace("1","#"))


def drop_rocks(count: int, jets: str) -> list[int]:
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
    rows = [0x01, 0x01, 0x01, 0x01]
    jet = 0
    pos = 3
    for r in range(count):
        rock = rocks[r % 5]
        row_mask = 0x01_01_01_01
        while True:
            # shift if not blocked
            d = jets[jet]
            s = rock >> 1 if d == ">" else rock << 1
            if not s & row_mask:
                rock = s

            jet += 1
            if jet >= len(jets):
                jet = 0

            if pos == 0 or (rock & ((row_mask << 8) | rows[pos - 1])):
                break
            pos -= 1
            # print(f"rock falls to {pos}")
            row_mask = (row_mask << 8) | rows[pos]

        for i in range(4):
            row = pos + i
            val = rock & 0xFF
            if row < len(rows):
                rows[row] |= val
            else:
                rows.append(val | 1)
            rock >>= 8

        while rows[-3:] != [0x01,0x01,0x01]:
            rows.append(0x01)

        pos = len(rows)
    return rows


jets = open("./day17.input").read().rstrip("\n")
# jets = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

board = drop_rocks(2022,jets)
print(len(board)-3)
