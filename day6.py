#!/usr/bin/env python3

def findMsgStart(data: str, markerLen: int) -> int:
    window = set()
    window_start, window_end = 0, 0
    while window_end < len(data):
        if len(window) == markerLen:
            return window_end
        right = data[window_end]
        while right in window:
            left = data[window_start]
            window.remove(left)
            window_start += 1
        window.add(right)
        window_end += 1
    return -1


def check():
    test_cases = [
        ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5, 23),
        ("nppdvjthqldpwncqszvftbrmjlhg", 6, 23),
        ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, 29),
        ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, 26),
    ]

    for t in test_cases:
        p1_actual = findMsgStart(t[0], 4)
        if p1_actual != t[1]:
            print(f"FAIL: part 1: expected {t[1]}, got {p1_actual} for {t[0]}")
        else:
            print("PASS")
        p2_actual = findMsgStart(t[0], 14)
        if p2_actual != t[2]:
            print(f"FAIL: part 2: expected {t[2]}, got {p2_actual} for {t[0]}")
        else:
            print("PASS")


if __name__ == "__main__":
    with open("./day6.input") as f:
        datastream = f.read().rstrip("\n")
    print(f"Part 1: {findMsgStart(datastream, 4)}, Part 2: {findMsgStart(datastream, 14)}")
