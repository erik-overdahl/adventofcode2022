#!/usr/bin/env python3


with open("./day5.input") as f:
    blob = f.read()

# blob = """
#     [D]
# [N] [C]
# [Z] [M] [P]
#  1   2   3

# move 1 from 2 to 1
# move 3 from 1 to 3
# move 2 from 2 to 1
# move 1 from 1 to 2
# """

cargo = []
moves = []

stacks, instructions = blob.split("\n\n")
stack_lines = stacks.split("\n")
for line in stack_lines[:-1]:
    num_line_crates = len(line)//4
    if len(cargo) <= num_line_crates:
        cargo += [""]*(num_line_crates - len(cargo) + 1)
    for i in range(0, len(line), 4):
        crate = line[i:i+4]
        if crate[0] == "[":
            cargo[i//4] += crate[1]
instruction_lines = instructions.split("\n")
for line in instruction_lines[:-1]:
    pieces = line.split(" ")
    moves.append((int(pieces[1]), int(pieces[3]) - 1, int(pieces[5]) - 1))

cargo2 = cargo.copy()

for m in moves:
    amount = m[0]
    orig = m[1]
    dest = m[2]

    moved = cargo[orig][:amount]
    cargo[dest] = moved[::-1] + cargo[dest]
    cargo[orig] = cargo[orig][amount:]

    moved2 = cargo2[orig][:amount]
    cargo2[dest] = moved2 + cargo2[dest]
    cargo2[orig] = cargo2[orig][amount:]


part1 = ''.join([s[0] for s in cargo])
part2 = ''.join([s[0] for s in cargo2])
print(f"Part 1: ({part1}), Part 2: ({part2})")
