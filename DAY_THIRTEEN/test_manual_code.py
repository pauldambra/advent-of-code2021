from pathlib import Path
from unittest import TestCase

example_instructions = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""


def get_grid_from(instructions: str) -> dict[int, dict[int, bool]]:
    # assume lookup speed is going to matter
    grid: dict[int, dict[int, bool]] = {}
    for line in instructions.split("\n\n")[0].splitlines():
        [x, y] = line.split(",")
        x = int(x)
        y = int(y)
        if y not in grid:
            grid[y] = {}
        grid[y][x] = True

    return grid


def get_folds_from(instructions: str) -> list[tuple[str, int]]:
    return [
        (instruction[0], int(instruction[1]))
        for instruction in [
            tuple(pair.split("="))
            for pair in [s[11:] for s in (instructions.split("\n\n")[1].splitlines())]
        ]
    ]


def fold_grid(
    grid: dict[int, dict[int, bool]], fold: tuple[str, int]
) -> dict[int, dict[int, bool]]:
    if fold[0] == "y":
        new_grid: dict[int, dict[int, bool]] = {}

        for y, row in grid.items():
            diff = y - fold[1]
            if diff > 0:
                target_y = fold[1] - diff
            else:
                target_y = y

            for x, item in row.items():
                if target_y not in new_grid:
                    new_grid[target_y] = {}
                new_grid[target_y][x] = item

        return new_grid

    else:
        new_grid: dict[int, dict[int, bool]] = {}
        for y, row in grid.items():
            for x, item in row.items():
                diff = fold[1] - x
                if diff < 0:  # point is to right of fold
                    target_x = fold[1] + diff
                else:
                    target_x = x

                if y not in new_grid:
                    new_grid[y] = {}
                new_grid[y][target_x] = item

        return new_grid


def draw_grid(grid: dict[int, dict[int, bool]]) -> str:
    max_y = max(grid.keys())
    max_x = 0
    for row in grid.values():
        row_max_x = max(row.keys())
        max_x = max(max_x, row_max_x)
    drawing = ""
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            drawing += "#" if grid.get(y, {}).get(x, False) else "."
        drawing += "\n"
    return drawing


class TestManualCode(TestCase):
    def test_can_make_a_grid(self):
        grid = get_grid_from(example_instructions)
        assert grid[10][6] is True

        assert (
            draw_grid(grid)
            == """...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........
"""
        )

    def test_can_read_fold_instructions(self):
        folds = get_folds_from(example_instructions)
        assert folds == [("y", 7), ("x", 5)]

    def test_can_fold_grid(self):
        grid = get_grid_from(example_instructions)
        folds = get_folds_from(example_instructions)

        assert grid.get(0, {}).get(0, False) is False

        grid = fold_grid(grid, folds[0])
        assert grid.get(0, {}).get(0, False) is True

        assert (
            draw_grid(grid)
            == """#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
"""
        )

        assert grid.get(0, {}).get(4, False) is False
        grid = fold_grid(grid, folds[1])
        assert grid.get(0, {}).get(4, False) is True

        assert (
            draw_grid(grid)
            == """#####
#...#
#...#
#...#
#####
"""
        )

    def test_how_many_visible_dots_in_example(self):
        grid = get_grid_from(example_instructions)
        folds = get_folds_from(example_instructions)

        grid = fold_grid(grid, folds[0])

        drawn_dots = 0
        for row in grid.values():
            drawn_dots += len(row.values())

        assert drawn_dots == 17

    def test_how_many_visible_dots_in_puzzle(self):
        puzzle_input_path = Path(__file__).parent / "./puzzle.input"
        with open(puzzle_input_path, "r", newline="\n") as f:
            instructions = f.read()
            grid = get_grid_from(instructions)
            folds = get_folds_from(instructions)

            grid = fold_grid(grid, folds[0])

            drawn_dots = 0
            for row in grid.values():
                drawn_dots += len(row.values())

            assert drawn_dots == 814

    def test_finish_folding_the_puzzle(self):
        puzzle_input_path = Path(__file__).parent / "./puzzle.input"
        with open(puzzle_input_path, "r", newline="\n") as f:
            instructions = f.read()
            grid = get_grid_from(instructions)
            folds = get_folds_from(instructions)

            for fold in folds:
                grid = fold_grid(grid, fold)

            assert (
                draw_grid(grid)
                == """###..####.####.#..#.###...##..####.###.
#..#....#.#....#..#.#..#.#..#.#....#..#
#..#...#..###..####.#..#.#..#.###..#..#
###...#...#....#..#.###..####.#....###.
#....#....#....#..#.#.#..#..#.#....#.#.
#....####.####.#..#.#..#.#..#.####.#..#"""
            )
