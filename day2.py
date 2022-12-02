#!/usr/bin/env python3

# rock < paper < scissors < rock
#
# rock:     0 A X
# paper:    1 B Y
# scissors: 2 C Z
#
# 0 0 -> draw
# 1 1 -> draw
# 2 2 -> draw
#
# 0 1 -> win
# 1 2 -> win
# 2 0 -> win
#
# 0 2 -> loss
# 1 0 -> loss
# 2 1 -> loss
#

def score_part1(line: str) -> int:
    theirs, ours = ord(line[0]) - 65, ord(line[2]) - 88
    result = 0
    if theirs == ours:
        result = 3
    elif (theirs + 1) % 3 == ours:
        result = 6
    return result + ours + 1

# X = lose, Y = draw, Z = win
def score_part2(line: str) -> int:
    theirs, result = ord(line[0]) - 65, (ord(line[2]) - 88) * 3
    choice = theirs
    if result < 3:
        choice = (theirs - 1) % 3
    elif result > 3:
        choice = (theirs + 1) % 3
    return result + choice + 1


with open("./day2.input") as f:
    lines = f.readlines()
    part1 = sum(map(score_part1, lines))
    part2 = sum(map(score_part2, lines))
    print(f"Part 1: {part1}, Part 2: {part2}")
