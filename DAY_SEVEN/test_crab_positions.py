from pathlib import Path
from unittest import TestCase


def positions_of(crabs_positions: str) -> list[int]:
    return [int(c) for c in crabs_positions.split(",")]


def max_from(crabs: str) -> int:
    return max(positions_of(crabs))


def distance_between(a: int, b: int) -> int:
    return abs(a - b)


def distances_for(positions: list[int], target: int) -> list[int]:
    return [distance_between(p, target) for p in positions]


def cost_of(distances: list[int]) -> int:
    return sum(distances)


def get_cheapest_fuel_cost(crabs: str):
    max_target = max_from(crabs)
    current_smallest = 2000000
    for n in range(0, max_target + 1):
        cost = cost_of(distances_for(positions_of(crabs), n))
        if cost < current_smallest:
            current_smallest = cost
    return current_smallest


class TestCrabPositions(TestCase):
    def test_can_get_max_from_crabs(self):
        crabs = "16,1,2,0,4,2,7,1,2,14"
        assert max_from(crabs) == 16

    def test_can_get_distance_between(self):
        assert distance_between(16, 2) == 14
        assert distance_between(106, 87) == 19
        assert distance_between(87, 106) == 19

    def test_can_get_distance_cost_for_whole_list(self):
        distances = distances_for([16, 1, 2, 0], 2)
        assert distances == [14, 1, 0, 2]
        cost = cost_of(distances)
        assert cost == 17

    def test_can_get_cost_of_example(self):
        cost = cost_of(distances_for(positions_of("16,1,2,0,4,2,7,1,2,14"), 2))
        assert cost == 37

    def test_how_should_this_work(self):
        crabs = "16,1,2,0,4,2,7,1,2,14"
        current_smallest = get_cheapest_fuel_cost(crabs)

        assert current_smallest == 37

    def test_for_puzzle_input(self):
        puzzle_input_path = Path(__file__).parent / "./puzzle.input"
        with open(puzzle_input_path, "r", newline="\n") as f:
            assert get_cheapest_fuel_cost(f.read()) == 348996
