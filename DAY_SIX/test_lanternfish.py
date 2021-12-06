from unittest import TestCase

puzzle_input = [
    5,
    1,
    5,
    3,
    2,
    2,
    3,
    1,
    1,
    4,
    2,
    4,
    1,
    2,
    1,
    4,
    1,
    1,
    5,
    3,
    5,
    1,
    5,
    3,
    1,
    2,
    4,
    4,
    1,
    1,
    3,
    1,
    1,
    3,
    1,
    1,
    5,
    1,
    5,
    4,
    5,
    4,
    5,
    1,
    3,
    2,
    4,
    3,
    5,
    3,
    5,
    4,
    3,
    1,
    4,
    3,
    1,
    1,
    1,
    4,
    5,
    1,
    1,
    1,
    2,
    1,
    2,
    1,
    1,
    4,
    1,
    4,
    1,
    1,
    3,
    3,
    2,
    2,
    4,
    2,
    1,
    1,
    5,
    3,
    1,
    3,
    1,
    1,
    4,
    3,
    3,
    3,
    1,
    5,
    2,
    3,
    1,
    3,
    1,
    5,
    2,
    2,
    1,
    2,
    1,
    1,
    1,
    3,
    4,
    1,
    1,
    1,
    5,
    4,
    1,
    1,
    1,
    4,
    4,
    2,
    1,
    5,
    4,
    3,
    1,
    2,
    5,
    1,
    1,
    1,
    1,
    2,
    1,
    5,
    5,
    1,
    1,
    1,
    1,
    3,
    1,
    4,
    1,
    3,
    1,
    5,
    1,
    1,
    1,
    5,
    5,
    1,
    4,
    5,
    4,
    5,
    4,
    3,
    3,
    1,
    3,
    1,
    1,
    5,
    5,
    5,
    5,
    1,
    2,
    5,
    4,
    1,
    1,
    1,
    2,
    2,
    1,
    3,
    1,
    1,
    2,
    4,
    2,
    2,
    2,
    1,
    1,
    2,
    2,
    1,
    5,
    2,
    1,
    1,
    2,
    1,
    3,
    1,
    3,
    2,
    2,
    4,
    3,
    1,
    2,
    4,
    5,
    2,
    1,
    4,
    5,
    4,
    2,
    1,
    1,
    1,
    5,
    4,
    1,
    1,
    4,
    1,
    4,
    3,
    1,
    2,
    5,
    2,
    4,
    1,
    1,
    5,
    1,
    5,
    4,
    1,
    1,
    4,
    1,
    1,
    5,
    5,
    1,
    5,
    4,
    2,
    5,
    2,
    5,
    4,
    1,
    1,
    4,
    1,
    2,
    4,
    1,
    2,
    2,
    2,
    1,
    1,
    1,
    5,
    5,
    1,
    2,
    5,
    1,
    3,
    4,
    1,
    1,
    1,
    1,
    5,
    3,
    4,
    1,
    1,
    2,
    1,
    1,
    3,
    5,
    5,
    2,
    3,
    5,
    1,
    1,
    1,
    5,
    4,
    3,
    4,
    2,
    2,
    1,
    3,
]


def parse_list_to_dict(ns: list[int]) -> dict[int, int]:
    result = {}
    for n in ns:
        if n not in result:
            result[n] = 0
        result[n] += 1

    return result


example_input = {1: 1, 2: 1, 3: 2, 4: 1}


def tick(fish: dict[int, int], times: int) -> dict[int, int]:
    current = fish
    for x in range(1, times + 1):
        next_fish = {}
        for n in range(8, -1, -1):
            if n != 0:
                next_fish[n - 1] = current.get(n, 0)
            else:
                birthing = current.get(0, 0)
                next_fish[6] += birthing
                next_fish[8] = next_fish.get(8, 0) + birthing

        current = next_fish

    return current


class TestLanternFish(TestCase):
    def test_single_fish_one_tick(self):
        fish = tick({3: 1}, times=1)
        assert fish == {0: 0, 1: 0, 2: 1, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}

    def test_single_fish_three_tick(self):
        fish = tick({3: 1}, times=3)
        assert fish == {0: 1, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}

    def test_single_fish_four_ticks(self):
        fish = tick({3: 1}, times=4)
        assert fish == {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 1, 7: 0, 8: 1}

    def test_example_two_ticks(self):
        fish = tick(example_input, times=2)  # after 2 days

        assert fish == {0: 1, 1: 2, 2: 1, 3: 0, 4: 0, 5: 0, 6: 1, 7: 0, 8: 1}

    def test_example_four_ticks(self):
        fish = tick(example_input, times=4)
        assert fish == {
            0: 1,
            1: 0,
            2: 0,
            3: 0,
            4: 1,
            5: 1,
            6: 3,
            7: 1,
            8: 2,
        }  # after 4 days 6,0,6,4,5,6,7,8,8

    def test_example_six_ticks(self):
        fish = tick(example_input, times=6)
        assert fish == {
            0: 0,
            1: 0,
            2: 1,
            3: 1,
            4: 3,
            5: 2,
            6: 2,
            7: 1,
            8: 0,
        }  # after 6 days

    def test_example_eight_ticks(self):
        fish = tick(example_input, times=8)
        assert fish == {
            0: 1,
            1: 1,
            2: 3,
            3: 2,
            4: 2,
            5: 1,
            6: 0,
            7: 0,
            8: 0,
        }  # after 8 days

    def test_example_ten_ticks(self):
        fish = tick(example_input, times=10)
        assert fish == {
            0: 3,
            1: 2,
            2: 2,
            3: 1,
            4: 0,
            5: 1,
            6: 1,
            7: 1,
            8: 1,
        }  # after 10 days

    def test_example_eighteen_ticks(self):
        fish = tick(example_input, times=18)

        assert sum(fish.values()) == 26

    def test_example_eighty_ticks(self):
        fish = tick(example_input, times=80)

        assert sum(fish.values()) == 5934

    def test_puzzle_input(self):
        fish = tick(parse_list_to_dict(puzzle_input), times=80)

        assert sum(fish.values()) == 362346

    def test_example_part_two(self):
        fish = tick(example_input, times=256)

        assert sum(fish.values()) == 26984457539

    def test_puzzle_input_part_two(self):
        fish = tick(parse_list_to_dict(puzzle_input), times=256)

        assert sum(fish.values()) == 1639643057051
