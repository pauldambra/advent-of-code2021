Grid = list[list[int]]
Coordinate = tuple[int, int]
LowPoints = list[tuple[int, Coordinate]]


def as_grid(grid_description: str) -> Grid:
    grid = []
    for line in grid_description.splitlines():
        grid.append([int(c) for c in list(line)])

    return grid


def find_neighbours(
    coordinate: Coordinate, max_row: int, max_col: int
) -> list[Coordinate]:
    (x, y) = coordinate
    candidate_neighbours = [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]
    neighbours = []
    for n in candidate_neighbours:
        if 0 <= n[0] <= max_col and 0 <= n[1] <= max_row:
            neighbours.append(n)
    return neighbours
