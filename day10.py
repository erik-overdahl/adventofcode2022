#!/usr/bin/env python3

def cpu_execute(instructions: list[str]) -> list[int]:
    X = 1
    values = []
    for op in instructions:
        values.append(X)
        if op != "noop":
            values.append(X)
            X += int(op[5:])
    return values


def signal_strengths(register_values: list[int]) -> list[int]:
    return [(i + 1) * value for i, value in enumerate(register_values)]


def final_screen(register_values: list[int]) -> str:
    pixels = ["."]*240
    for cycle, X in enumerate(register_values):
        if X-2 < cycle % 40 < X+2:
            pixels[cycle % 240] = "█"
    return '\n'.join([''.join(pixels[i:i+40]) for i in range(0, 240, 40)])


input = [line.rstrip("\n") for line in open("./day10.input")]

register_values = cpu_execute(input)
strengths = signal_strengths(register_values)
samples = [strengths[i-1] for i in range(20,221,40)]
screen = final_screen(register_values)

print(f"Part 1: {sum(samples)}, Part 2:\n{screen}")


def solve():
    """
    Alternatively, solve both parts in one pass
    """
    tokens = open("./day10.input").read().replace("\n", " ").split(" ")
    X = 1
    strength = 0
    pixels = [" "]*240
    for i, token in enumerate(tokens):
        line_pos = i%40
        if line_pos == 19:
            strength += (i + 1) * X
        if X - 2 < line_pos < X + 2:
            pixels[i % 240] = "█"
        if token != "noop" and token != "addx" and token != "":
            X += int(token)

    screen = '\n'.join([''.join(pixels[i:i+40]) for i in range(0, 240, 40)])
    print(f"Part 1: {strength}, Part 2:\n{screen}")
