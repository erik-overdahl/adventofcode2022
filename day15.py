#!/usr/bin/env python3

def parse_points(input: str) -> list[tuple[complex,complex]]:
    pairs = []
    for line in input.split("\n"):
        pieces = line.split(": ")
        t = pieces[0].split(" ")
        sensor = complex(int(t[-2][2:-1]), int(t[-1][2:]))
        t = pieces[1].split(" ")
        beacon = complex(int(t[-2][2:-1]), int(t[-1][2:]))
        pairs.append((sensor, beacon))
    return pairs


def manhattan_distance(sensor: complex, beacon: complex) -> int:
    dx = abs(sensor.real - beacon.real)
    dy = abs(sensor.imag - beacon.imag)
    return int(dx + dy)


def sensor_coverage_at_y(pair: tuple[complex,complex], y: int) -> tuple[complex,complex]|tuple[()]:
    sensor, beacon = pair
    manhattan = manhattan_distance(sensor, beacon)
    y_dist = abs(sensor.imag - y)
    if y_dist > manhattan:
        return ()
    x_dist = manhattan - y_dist
    return (complex(sensor.real - x_dist, y), complex(sensor.real + x_dist, y))


def coverage_at_y(pairs: list[tuple[complex, complex]], y: int) -> int:
    segments = []
    for p in pairs:
        line = sensor_coverage_at_y(p, y)
        if len(line) > 0:
            segments.append(line)

    segments.sort(key=lambda s: s[0].real)

    num_points = 0
    l, r = segments[0]
    num_points += abs(r.real - l.real)
    for s in segments[1:]:
        l = s[0] if s[0].real > r.real else r
        if s[1].real <= r.real:
            continue
        r = s[1]
        num_points += abs(r.real - l.real)
    return int(num_points)


input = open("./day15.input").read().rstrip("\n")

pairs = parse_points(input)

print(f"Part 1: {coverage_at_y(pairs, 2000000)}")
