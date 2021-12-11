import dataclasses
from queue import SimpleQueue
from unittest import TestCase

puzzle_input = """1172728874
6751454281
2612343533
1884877511
7574346247
2117413745
7766736517
4331783444
4841215828
6857766273"""

example_input = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""


@dataclasses.dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def neighbours(self) -> list["Coordinate"]:
        candidate_neighbours = [
            Coordinate(self.x - 1, self.y - 1),
            Coordinate(self.x, self.y - 1),
            Coordinate(self.x + 1, self.y - 1),
            Coordinate(self.x - 1, self.y),
            Coordinate(self.x + 1, self.y),
            Coordinate(self.x - 1, self.y + 1),
            Coordinate(self.x, self.y + 1),
            Coordinate(self.x + 1, self.y + 1),
        ]
        neighbours = []
        for n in candidate_neighbours:
            if 0 <= n.x < 10 and 0 <= n.y < 10:
                neighbours.append(n)
        return neighbours


class Cavern:
    def __init__(self, grid: str):
        self.current_step = 0
        self.synchronised_at = -1
        self.grid = grid
        self.positions = []
        self.flashes = 0
        for row_index, row in enumerate(grid.splitlines()):
            self.positions.append([int(r) for r in list(row)])

    def __getitem__(self, coord: Coordinate) -> int:
        return self.positions[coord.y][coord.x]

    def __setitem__(self, coord: Coordinate, value: int) -> None:
        self.positions[coord.y][coord.x] = value

    def step(self):
        self.current_step += 1

        for y in range(10):
            for x in range(10):
                self.positions[y][x] += 1

        flashed = {}
        has_flashed = SimpleQueue()
        for y in range(10):
            for x in range(10):
                coord = Coordinate(x, y)
                if self[coord] > 9:
                    flashed[coord] = True
                    has_flashed.put(coord)

        while not has_flashed.empty():
            flasher = has_flashed.get()
            for n in flasher.neighbours():
                self[n] += 1
                if self[n] > 9 and n not in flashed:
                    flashed[n] = True
                    has_flashed.put(n)

        self.flashes += len(flashed)

        if len(flashed) == 100:
            self.synchronised_at = self.current_step

        for coord in flashed:
            self[coord] = 0

    def __str__(self) -> str:
        grid = ""
        for row in self.positions:
            grid += "".join([str(r) for r in row]) + "\n"
        return grid


class TestOctopuses(TestCase):
    def test_two_steps(self):
        cavern = Cavern(example_input)
        assert cavern[Coordinate(0, 0)] == 5
        cavern.step()
        assert cavern[Coordinate(0, 0)] == 6
        assert cavern[Coordinate(2, 0)] == 9
        assert cavern.flashes == 0
        cavern.step()
        assert cavern[Coordinate(2, 0)] == 0
        assert cavern[Coordinate(1, 0)] == 8
        assert cavern.flashes == 35

    def test_ten_steps(self):
        cavern = Cavern(example_input)
        for _ in range(10):
            cavern.step()

        assert cavern.flashes == 204

    def test_hundred_steps(self):
        cavern = Cavern(example_input)
        for _ in range(100):
            cavern.step()

        assert cavern.flashes == 1656

    def test_hundred_steps_from_puzzle_input(self):
        cavern = Cavern(puzzle_input)
        for _ in range(100):
            cavern.step()

        assert cavern.flashes == 1644

    def test_first_synchronised_flash(self):
        cavern = Cavern(example_input)
        while cavern.synchronised_at == -1:
            cavern.step()

        assert cavern.synchronised_at == 195

    def test_first_synchronised_flash_for_puzzle_input(self):
        cavern = Cavern(puzzle_input)
        while cavern.synchronised_at == -1:
            cavern.step()

        assert cavern.synchronised_at == 229
