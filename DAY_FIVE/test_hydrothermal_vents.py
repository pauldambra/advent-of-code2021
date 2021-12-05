from dataclasses import dataclass
from enum import Enum, auto
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


class Ordinal(Enum):
    NORTH = auto()
    NORTH_EAST = auto()
    EAST = auto()
    SOUTH_EAST = auto()
    SOUTH = auto()
    SOUTH_WEST = auto()
    WEST = auto()
    NORTH_WEST = auto()

    def is_diagonal(self):
        return (
            self == Ordinal.NORTH_EAST
            or self == Ordinal.SOUTH_EAST
            or self == Ordinal.SOUTH_WEST
            or self == Ordinal.NORTH_WEST
        )


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def move(self, direction: Ordinal, allow_diagonals: bool = False) -> "Coordinate":
        match direction:
            case Ordinal.NORTH:
                return Coordinate(self.x, self.y - 1)
            case Ordinal.NORTH_EAST:
                return Coordinate(self.x + 1, self.y - 1) if allow_diagonals else None
            case Ordinal.EAST:
                return Coordinate(self.x + 1, self.y)
            case Ordinal.SOUTH_EAST:
                return Coordinate(self.x + 1, self.y + 1) if allow_diagonals else None
            case Ordinal.SOUTH:
                return Coordinate(self.x, self.y + 1)
            case Ordinal.SOUTH_WEST:
                return Coordinate(self.x - 1, self.y + 1) if allow_diagonals else None
            case Ordinal.WEST:
                return Coordinate(self.x - 1, self.y)
            case Ordinal.NORTH_WEST:
                return Coordinate(self.x - 1, self.y - 1) if allow_diagonals else None

    @staticmethod
    def direction_between(start: "Coordinate", end: "Coordinate") -> Ordinal:
        if start.x < end.x and start.y == end.y:
            return Ordinal.EAST
        if start.x < end.x and start.y < end.y:
            return Ordinal.SOUTH_EAST
        if start.x == end.x and start.y < end.y:
            return Ordinal.SOUTH
        if start.x > end.x and start.y < end.y:
            return Ordinal.SOUTH_WEST
        if start.x > end.x and start.y == end.y:
            return Ordinal.WEST
        if start.x > end.x and start.y > end.y:
            return Ordinal.NORTH_WEST
        if start.x == end.x and start.y > end.y:
            return Ordinal.NORTH
        if start.x < end.x and start.y > end.y:
            return Ordinal.NORTH_EAST

    @staticmethod
    def parse(coordinate_description: str) -> "Coordinate":
        parts = coordinate_description.split(",")
        return Coordinate(int(parts[0]), int(parts[1]))


def as_line(
    nearby_vent_description: str, allow_diagonals: bool = False
) -> Optional[list[Coordinate]]:
    [left, right] = nearby_vent_description.split(" -> ")
    start = Coordinate.parse(left)
    end = Coordinate.parse(right)
    return make_line(start, end, allow_diagonals)


def make_line(
    start: Coordinate, end: Coordinate, allow_diagonals: bool = False
) -> Optional[list[Coordinate]]:
    direction = Coordinate.direction_between(start, end)
    if not allow_diagonals and direction.is_diagonal():
        return None

    line = [start]
    previous = start
    while previous != end:
        current = previous.move(direction, allow_diagonals)
        line.append(current)
        previous = current

    return line


def find_overlaps(lines: list[list[Coordinate] | None]) -> dict[Coordinate, int]:
    overlaps: dict[Coordinate, int] = {}
    present_lines = [line for line in lines if line]
    for line in present_lines:
        for coord in line:
            if coord not in overlaps:
                overlaps[coord] = 0

            overlaps[coord] = overlaps[coord] + 1

    return overlaps


class TestHydrothermalVents(TestCase):
    def test_can_parse_one_horizontal_line(self):
        line = as_line("""0,4 -> 5,4""")
        assert line == [
            Coordinate(0, 4),
            Coordinate(1, 4),
            Coordinate(2, 4),
            Coordinate(3, 4),
            Coordinate(4, 4),
            Coordinate(5, 4),
        ]

    def test_can_parse_one_vertical_line(self):
        line = as_line("""4, 0 -> 4, 5""")
        assert line == [
            Coordinate(4, 0),
            Coordinate(4, 1),
            Coordinate(4, 2),
            Coordinate(4, 3),
            Coordinate(4, 4),
            Coordinate(4, 5),
        ]

    def test_can_parse_backwards_vertical_line(self):
        line = as_line("""4, 5 -> 4, 0""")
        assert line == [
            Coordinate(4, 5),
            Coordinate(4, 4),
            Coordinate(4, 3),
            Coordinate(4, 2),
            Coordinate(4, 1),
            Coordinate(4, 0),
        ]

    def test_can_parse_backwards_horizontal_line(self):
        line = as_line("""9, 4 -> 2, 4""")
        assert line == [
            Coordinate(9, 4),
            Coordinate(8, 4),
            Coordinate(7, 4),
            Coordinate(6, 4),
            Coordinate(5, 4),
            Coordinate(4, 4),
            Coordinate(3, 4),
            Coordinate(2, 4),
        ]

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

    def test_can_parse_diagonal_line(self):
        line = as_line("""1,1 -> 3,3""", allow_diagonals=True)
        assert line == [Coordinate(1, 1), Coordinate(2, 2), Coordinate(3, 3)]

    def test_can_parse_backwards_diagonal_line(self):
        line = as_line("""9,7 -> 7,9""", allow_diagonals=True)
        assert line == [Coordinate(9, 7), Coordinate(8, 8), Coordinate(7, 9)]

    def test_example_input_with_diagonals(self):
        lines = [
            as_line(line, allow_diagonals=True)
            for line in example_input.splitlines()
            if line
        ]
        overlaps = find_overlaps(lines)
        two_or_more = sum([1 for v in overlaps.values() if v >= 2])
        assert two_or_more == 12

    def test_puzzle_input_with_diagonals(self):
        puzzle_input_path = Path(__file__).parent / "./puzzle.input"
        with open(puzzle_input_path, "r", newline="\n") as f:
            lines = [
                as_line(line, allow_diagonals=True)
                for line in f.read().splitlines()
                if line
            ]
            overlaps = find_overlaps(lines)
            two_or_more = sum([1 for v in overlaps.values() if v >= 2])
            assert two_or_more == 20012
