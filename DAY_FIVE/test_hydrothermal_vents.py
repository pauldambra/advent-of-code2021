from pathlib import Path
from typing import Optional
from unittest import TestCase

example_input = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""


def as_coordinate(coordinate_description: str) -> tuple[int, int]:
    parts = coordinate_description.split(",")
    return int(parts[0]), int(parts[1])


def as_line(nearby_vent_description: str) -> Optional[list[tuple]]:
    [left, right] = nearby_vent_description.split(" -> ")
    start = as_coordinate(left)
    end = as_coordinate(right)
    is_horizontal = start[0] != end[0] and start[1] == end[1]
    is_vertical = start[0] == end[0] and start[1] != end[1]
    is_increasing = start[0] < end[0] if is_horizontal else start[1] < end[1]

    if is_horizontal:  # is horizontal
        line = make_horizontal_line(start, end, is_increasing)
    elif is_vertical:  # must be vertical
        line = make_vertical_line(start, end, is_increasing)
    else:
        line = None

    return line


def make_vertical_line(start, end, is_increasing):
    if is_increasing:
        first = start
        last = end
    else:
        first = end
        last = start

    line = []

    for y in range(first[1], last[1] + 1):
        line.append((first[0], y))

    return line


def make_horizontal_line(start, end, is_increasing):
    if is_increasing:
        first = start
        last = end
    else:
        first = end
        last = start

    line = []

    for x in range(first[0], last[0] + 1):
        line.append((x, start[1]))

    return line


def find_overlaps(lines):
    overlaps: dict[tuple, int] = {}
    for line in lines:
        if line:
            for coord in line:
                if coord not in overlaps:
                    overlaps[coord] = 0

                overlaps[coord] = overlaps[coord] + 1

    return overlaps


class TestHydrothermalVents(TestCase):
    def test_can_parse_one_horizontal_line(self):
        line = as_line("""0,4 -> 5,4""")
        assert line == [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4)]

    def test_can_parse_one_vertical_line(self):
        line = as_line("""4, 0 -> 4, 5""")
        assert line == [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5)]

    def test_can_parse_backwards_vertical_line(self):
        line = as_line("""4, 5 -> 4, 0""")
        assert line == [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5)]

    def test_can_parse_backwards_horizontal_line(self):
        line = as_line("""9, 4 -> 2, 4""")
        assert line == [(2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4)]

    def test_example_input(self):
        lines = [as_line(line) for line in example_input.splitlines() if line]
        overlaps = find_overlaps(lines)
        two_or_more = sum([1 for v in overlaps.values() if v >= 2])
        assert two_or_more == 5

    def test_puzzle_input(self):
        puzzle_input_path = Path(__file__).parent / "./puzzle.input"
        with open(puzzle_input_path, "r", newline="\n") as f:
            lines = [as_line(line) for line in f.read().splitlines() if line]
            overlaps = find_overlaps(lines)
            two_or_more = sum([1 for v in overlaps.values() if v >= 2])
            assert two_or_more == 7142
