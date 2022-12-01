#!/usr/bin/env python3

elf_cals = []

with open("./day1.input") as f:
    elf = []
    for line in f:
        line = line.rstrip("\n")
        if len(line) == 0:
            elf_cals.append(elf)
            elf = []
            continue
        elf.append(int(line))

elf_cal_sums = list(map(sum, elf_cals))
elf_cal_sums.sort(reverse=True)

print(f"Part 1: {elf_cal_sums[0]}, Part 2: {sum(elf_cal_sums[:3])}")
