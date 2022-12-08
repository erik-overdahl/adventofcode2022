#!/usr/bin/env python3

def count_visible(trees: list[str]) -> int:
    line_len = len(trees[0])
    col_len = len(trees)
    visible = [0]*(line_len*col_len)
    # max height seen for each col as we move down
    col_maxes = [trees[0]]

    for i in range(1,col_len-1):
        line = trees[i]

        prev_line_col_maxes = col_maxes[-1]
        d_max = " "

        l_max = line[0]
        for j in range(1,line_len - 1):
            height = line[j]
            # visible from left?
            if height > l_max[-1]:
                visible[(i*line_len)+j] = 1
                l_max += height
            else:
                l_max += l_max[-1]
            # visible from top?
            if height > prev_line_col_maxes[j]:
                visible[(i*line_len)+j] = 1
                d_max += height
            else:
                d_max += prev_line_col_maxes[j]

        col_maxes.append(d_max)

        r_max = line[-1]
        for j in range(line_len - 2, 0, -1):
            height = line[j]
            # visible from right?
            if height > r_max:
                visible[(i*line_len)+j] = 1
                r_max = height
            if height >= l_max[j]:
                # no tree to the left of this could be visible from right, exit early
                break

    cols_considered = [i for i in range(1,line_len-1)]
    b_max = list(trees[-1])

    for i in range(col_len - 2, 1, -1):
        line = trees[i]
        t_max = col_maxes[i]
        next = []
        for j in cols_considered:
            height, below_height = line[j], b_max[j]
            if height > below_height:
                visible[(i*line_len)+j] = 1
                b_max[j] = height
            if height < t_max[j]:
                next.append(j)
        if len(next) == 0:
            break
        cols_considered = next

    return 2*line_len + 2*(col_len-2) + sum(visible)


input = []
for line in open("./day8.input"):
    input.append(line.rstrip("\n"))

# input = [
#     "30373",
#     "25512",
#     "65332",
#     "33549",
#     "35390",
# ]

print(f"Part 1: {count_visible(input)}")
