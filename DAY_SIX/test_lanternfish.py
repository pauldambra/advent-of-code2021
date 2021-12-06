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


# from https://stackoverflow.com/a/9671301/222163
def grouper(iterable: list[int], n: int = 500) -> list[list[int]]:
    return [iterable[x : x + n] for x in range(0, len(iterable), n)]


fish_fridge: dict[tuple[int], tuple[list[int], int]] = {}


def tick(fish: list[int]) -> list[int]:
    next_tick = []
    new_fish = 0
    for group in grouper(fish):
        if tuple(group) not in fish_fridge:
            chunk = []
            new_fish_chunk = 0
            for f in group:
                if f == 0:
                    chunk.append(6)
                    new_fish_chunk += 1
                elif f:
                    chunk.append(f - 1)

            fish_fridge[tuple(group)] = (chunk, new_fish_chunk)
        else:
            (chunk, new_fish_chunk) = fish_fridge[tuple(group)]

        next_tick += chunk
        new_fish += new_fish_chunk

    return next_tick + [8] * new_fish


class TestLanternFish(TestCase):
    def test_single_fish(self):
        fish = [3]
        fish = tick(fish)
        assert fish == [2]

        fish = tick(tick(fish))
        assert fish == [0]

        fish = tick(fish)
        assert fish == [6, 8]

    def test_a_list_of_fish(self):
        fish = [3, 4, 3, 1, 2]
        fish = tick(tick(fish))  # after 2 days

        assert fish == [1, 2, 1, 6, 0, 8]

        fish = tick(tick(fish))
        assert fish == [6, 0, 6, 4, 5, 6, 7, 8, 8]  # after 4 days

        fish = tick(tick(fish))
        assert fish == [4, 5, 4, 2, 3, 4, 5, 6, 6, 7]  # after 6 days

        fish = tick(tick(fish))
        assert fish == [2, 3, 2, 0, 1, 2, 3, 4, 4, 5]  # after 8 days

        fish = tick(tick(fish))
        assert fish == [0, 1, 0, 5, 6, 0, 1, 2, 2, 3, 7, 8]  # after 10 days

        fish = [3, 4, 3, 1, 2]
        for n in range(0, 18):
            fish = tick(fish)

        assert len(fish) == 26

        fish = [3, 4, 3, 1, 2]
        for n in range(0, 80):
            fish = tick(fish)

        assert len(fish) == 5934

    def test_puzzle_input(self):
        fish = puzzle_input

        for n in range(0, 80):
            fish = tick(fish)

        assert len(fish) == 362346

    def test_example_part_two(self):
        fish = [3, 4, 3, 1, 2]
        for n in range(0, 256):
            fish = tick(fish)

        assert len(fish) == 26984457539
