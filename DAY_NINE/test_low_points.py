import math
from pathlib import Path
from queue import SimpleQueue
from unittest import TestCase

from lib.grid import Coordinate, Grid, as_grid, find_neighbours

example = """2199943210
3987894921
9856789892
8767896789
9899965678"""

LowPoints = list[tuple[int, Coordinate]]


def get_risk_levels_of_lowest_points(lower: LowPoints) -> list[int]:
    risk_levels = [1 + h for (h, coord) in lower]
    return risk_levels


def get_lowest_points(grid: Grid) -> LowPoints:
    lower = []
    for row_index, row in enumerate(grid):
        for col_index, height in enumerate(row):
            neighbours = find_neighbours(
                (col_index, row_index), max_row=len(grid) - 1, max_col=len(row) - 1
            )
            neighbour_heights = []
            for n in neighbours:
                neighbour_heights.append(grid[n[1]][n[0]])
            if all(height < nh for nh in neighbour_heights):
                lower.append((height, (col_index, row_index)))
    return lower


def get_basins(grid: Grid, lowest_points: list[Coordinate]) -> list[list[Coordinate]]:
    basins = []
    points_to_check = SimpleQueue()
    for point in lowest_points:
        basins.append([])
        basin = basins[-1]

        points_to_check.put(point)
        checked = []
        while not points_to_check.empty():
            next_point = points_to_check.get()
            if next_point not in checked:
                checked.append(next_point)
                if grid[next_point[1]][next_point[0]] < 9:
                    basin.append(next_point)
                    neighbours = find_neighbours(
                        next_point, max_row=len(grid) - 1, max_col=len(grid[0]) - 1
                    )
                    for neighbour in neighbours:
                        points_to_check.put(neighbour)
    return basins


class TestLowPoints(TestCase):
    def test_parse_to_grid(self):
        grid = as_grid(example)
        assert grid == [
            [2, 1, 9, 9, 9, 4, 3, 2, 1, 0],
            [3, 9, 8, 7, 8, 9, 4, 9, 2, 1],
            [9, 8, 5, 6, 7, 8, 9, 8, 9, 2],
            [8, 7, 6, 7, 8, 9, 6, 7, 8, 9],
            [9, 8, 9, 9, 9, 6, 5, 6, 7, 8],
        ]

    def test_find_adjacent_coords(self):
        coordinate = (2, 4)
        neighbours = find_neighbours(coordinate, max_row=5, max_col=3)
        assert neighbours == [(1, 4), (2, 3), (3, 4), (2, 5)]

    def test_ignore_impossible_neighbours(self):
        coordinate = (0, 4)
        neighbours = find_neighbours(coordinate, max_row=5, max_col=3)
        assert neighbours == [(0, 3), (1, 4), (0, 5)]

    def test_check_if_point_is_lower_than_neighbours(self):
        grid = as_grid(example)
        lower = get_lowest_points(grid)
        risk_levels = get_risk_levels_of_lowest_points(lower)
        assert sum(risk_levels) == 15
        assert risk_levels == [2, 1, 6, 6]

    def test_check_puzzle_input(self):
        puzzle_input_path = Path(__file__).parent / "./puzzle.input"
        with open(puzzle_input_path, "r", newline="\n") as f:
            grid = as_grid(f.read())
            lower = get_lowest_points(grid)
            risk_levels = get_risk_levels_of_lowest_points(lower)
            assert sum(risk_levels) == 480

    def test_find_basins_in_example(self):
        grid = as_grid(example)
        lowest_points = [coord for (h, coord) in get_lowest_points(grid)]
        basins = get_basins(grid, lowest_points)

        assert len(basins) == 4
        basins.sort(key=len, reverse=True)
        assert [len(x) for x in basins] == [14, 9, 9, 3]
        assert math.prod([len(x) for x in basins][0:3]) == 1134

    def test_find_basins_in_puzzle_input(self):
        puzzle_input_path = Path(__file__).parent / "./puzzle.input"
        with open(puzzle_input_path, "r", newline="\n") as f:
            grid = as_grid(f.read())
            lowest_points = [coord for (h, coord) in get_lowest_points(grid)]
            basins = get_basins(grid, lowest_points)
            basins.sort(key=len, reverse=True)
            top_three = [len(basin) for basin in basins[0:3]]
            assert math.prod(top_three) == 1045660
