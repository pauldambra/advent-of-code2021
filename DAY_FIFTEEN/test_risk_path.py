from pathlib import Path
from unittest import TestCase

from lib.grid import as_grid, find_neighbours

example_input = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""


class Graph:
    """from https://www.pythonpool.com/a-star-algorithm-python/"""

    def __init__(self, adjac_lis, heuristic):
        self.heuristic = heuristic
        self.adjac_lis = adjac_lis

    def get_neighbors(self, v):
        return self.adjac_lis[v]

    # This is heuristic function which is having equal values for all nodes
    def h(self, n: tuple[int, int]):
        return self.heuristic[n]

    def a_star_algorithm(
        self, start: tuple[int, int], stop: tuple[int, int]
    ) -> list[tuple[int, int]]:
        # In this open_lst is a lisy of nodes which have been visited, but who's
        # neighbours haven't all been always inspected, It starts off with the start
        # node
        # And closed_lst is a list of nodes which have been visited
        # and who's neighbors have been always inspected
        open_lst = {start}
        closed_lst = set([])

        # poo has present distances from start to all other nodes
        # the default value is +infinity
        poo = {start: 0}

        # par contains an adjac mapping of all nodes
        par = {}
        par[start] = start

        while len(open_lst) > 0:
            n = None

            # it will find a node with the lowest value of f() -
            for v in open_lst:
                if n is None or poo[v] + self.h(v) < poo[n] + self.h(n):
                    n = v

            if n is None:
                print("Path does not exist!")
                return None

            # if the current node is the stop
            # then we start again from start
            if n == stop:
                reconst_path = []

                while par[n] != n:
                    reconst_path.append(n)
                    n = par[n]

                reconst_path.append(start)

                reconst_path.reverse()

                print("Path found: {}".format(reconst_path))
                return reconst_path

            # for all the neighbors of the current node do
            for (m, weight) in self.get_neighbors(n):
                # if the current node is not presentin both open_lst and closed_lst
                # add it to open_lst and note n as it's par
                if m not in open_lst and m not in closed_lst:
                    open_lst.add(m)
                    par[m] = n
                    poo[m] = poo[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update par data and poo data
                # and if the node was in the closed_lst, move it to open_lst
                else:
                    if poo[m] > poo[n] + weight:
                        poo[m] = poo[n] + weight
                        par[m] = n

                        if m in closed_lst:
                            closed_lst.remove(m)
                            open_lst.add(m)

            # remove n from the open_lst, and add it to closed_lst
            # because all of his neighbors were inspected
            open_lst.remove(n)
            closed_lst.add(n)

        print("Path does not exist!")
        return None


def as_adjacency_list(
    grid: list[list[int]], max_y, max_x
) -> dict[tuple[int, int], list[tuple[tuple[int], int]]]:
    al = {}
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if (x, y) not in al:
                al[(x, y)] = []
            for n in find_neighbours((x, y), max_y, max_x):
                al[(x, y)].append((n, grid[n[1]][n[0]]))
    return al


def make_five_wide(grid: list[list[int]]) -> list[list[int]]:
    new_grid = []
    for row in grid:
        new_grid.append([])
        for i in range(5):
            for cell in row:
                new_value = cell + i
                if new_value > 9:
                    new_value -= 9
                new_grid[-1].append(new_value)

    return new_grid


def make_five_tall(grid: list[list[int]]) -> list[list[int]]:
    new_grid = []
    for i in range(5):
        for row in grid:
            new_grid.append([])
            for cell in row:
                new_value = cell + i
                if new_value > 9:
                    new_value -= 9

                new_grid[-1].append(new_value)

    return new_grid


class TestRiskPath(TestCase):
    def test_something(self):
        grid = as_grid(example_input)
        max_x = len(grid[0]) - 1
        max_y = len(grid) - 1
        adjacency_list = as_adjacency_list(grid, max_y, max_x)
        print(adjacency_list)
        heuristic = {k: grid[k[1]][k[0]] for k in adjacency_list.keys()}
        g = Graph(adjacency_list, heuristic)
        path = g.a_star_algorithm((0, 0), (max_x, max_y))
        scores = [grid[c[1]][c[0]] for c in path]

        assert scores == [
            1,
            1,
            2,
            1,
            3,
            6,
            5,
            1,
            1,
            1,
            5,
            1,
            1,
            3,
            2,
            3,
            2,
            1,
            1,
        ]

        assert sum(scores) - grid[0][0] == 40

    def test_puzzle_input_part_1(self):
        puzzle_input_path = Path(__file__).parent / "./puzzle.input"
        with open(puzzle_input_path, "r", newline="\n") as f:
            grid = as_grid(f.read())
            max_x = len(grid[0]) - 1
            max_y = len(grid) - 1
            adjacency_list = as_adjacency_list(grid, max_y, max_x)
            heuristic = {k: grid[k[1]][k[0]] for k in adjacency_list.keys()}
            g = Graph(adjacency_list, heuristic)
            path = g.a_star_algorithm((0, 0), (max_x, max_y))
            scores = [grid[c[1]][c[0]] for c in path]

            assert sum(scores) - grid[0][0] == 673

    def test_part_two_grid(self):
        grid = as_grid(example_input)
        grid = make_five_wide(grid)
        assert grid[0] == [
            1,
            1,
            6,
            3,
            7,
            5,
            1,
            7,
            4,
            2,
            2,
            2,
            7,
            4,
            8,
            6,
            2,
            8,
            5,
            3,
            3,
            3,
            8,
            5,
            9,
            7,
            3,
            9,
            6,
            4,
            4,
            4,
            9,
            6,
            1,
            8,
            4,
            1,
            7,
            5,
            5,
            5,
            1,
            7,
            2,
            9,
            5,
            2,
            8,
            6,
        ]

        grid = make_five_tall(grid)
        assert len(grid) == 50
        print(grid)
        assert grid[0][0] == 1
        assert grid[9][0] == 2
        assert grid[10][0] == 2
        assert grid[19][0] == 3
        assert grid[20][0] == 3
        assert grid[29][0] == 4
        assert grid[30][0] == 4
        assert grid[39][0] == 5
        assert grid[40][0] == 5
        assert grid[49][0] == 6

    def test_example_part_two_grid(self):
        grid = as_grid(example_input)
        grid = make_five_wide(grid)
        grid = make_five_tall(grid)
        max_x = len(grid[0]) - 1
        max_y = len(grid) - 1
        adjacency_list = as_adjacency_list(grid, max_y, max_x)
        heuristic = {k: grid[k[1]][k[0]] for k in adjacency_list.keys()}
        g = Graph(adjacency_list, heuristic)
        path = g.a_star_algorithm((0, 0), (max_x, max_y))
        scores = [grid[c[1]][c[0]] for c in path]

        assert sum(scores) - grid[0][0] == 315

    def test_puzzle_input_part_two_grid(self):
        puzzle_input_path = Path(__file__).parent / "./puzzle.input"
        with open(puzzle_input_path, "r", newline="\n") as f:
            grid = as_grid(f.read())
            grid = make_five_wide(grid)
            grid = make_five_tall(grid)
            max_x = len(grid[0]) - 1
            max_y = len(grid) - 1
            adjacency_list = as_adjacency_list(grid, max_y, max_x)
            heuristic = {k: grid[k[1]][k[0]] for k in adjacency_list.keys()}
            g = Graph(adjacency_list, heuristic)
            path = g.a_star_algorithm((0, 0), (max_x, max_y))
            scores = [grid[c[1]][c[0]] for c in path]

            assert sum(scores) - grid[0][0] == 2893
