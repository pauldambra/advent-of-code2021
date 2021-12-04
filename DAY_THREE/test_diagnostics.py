from pathlib import Path
from typing import Iterator, Callable
from unittest import TestCase

puzzle_input_path = Path(__file__).parent / "./puzzle.input"

example_input = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""


def as_columns(rows: Iterator[str]) -> Iterator[list[int]]:
    columns: list[list[int]] = []
    for row in rows:
        for index, c in enumerate(list(row.strip())):
            try:
                columns[index].append(int(c))
            except IndexError:
                columns.append([int(c)])

    for column in columns:
        yield column


def count_bits(columns: Iterator[list[int]]) -> dict[int, dict[int]]:
    grouped = {}
    for index, column in enumerate(columns):
        grouped[index] = {0: 0, 1: 0}
        for bit in column:
            if bit in grouped[index]:
                grouped[index][bit] += 1
            else:
                grouped[index][bit] = 1

    return grouped


def to_most_common_bits(counted_bits: dict[int, dict[int]]) -> list[int]:
    rates = []
    for column_count in counted_bits.values():
        rates.append(0 if column_count[0] > column_count[1] else 1)

    return rates


def to_least_common_bits(counted_bits: dict[int, dict[int]]) -> list[int]:
    rates = []
    for column_count in counted_bits.values():
        rates.append(1 if column_count[0] > column_count[1] else 0)

    return rates


def as_epsilon(bits: list[int]) -> list[int]:
    return [1 if x == 0 else 0 for x in bits]


def to_number(bits):
    return int("".join([str(i) for i in bits]), 2)


def get_rating(
    diagnostic_input: list[str],
    bit_comparison: Callable[[dict[int, dict[int]]], list[int]],
) -> int:
    candidates = diagnostic_input

    column_index = 0
    while len(candidates) != 1 and column_index <= len(candidates[0]):
        compared = bit_comparison(count_bits(as_columns(iter(candidates))))

        candidates = [
            c
            for c in candidates
            if list(c)[column_index] == str(compared[column_index])
        ]
        column_index += 1

    return to_number(candidates[0])


def get_o2_rating(diagnostic_input: list[str]) -> int:
    return get_rating(diagnostic_input, to_most_common_bits)


def get_co2_scrubber_rating(diagnostic_input: list[str]) -> int:
    return get_rating(diagnostic_input, to_least_common_bits)


class TestDiagnotics(TestCase):
    def test_read_as_columns(self):
        columns = [c for c in as_columns(iter(example_input.splitlines()))]
        assert columns[0] == [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0]

    def test_can_count_bits(self):
        counted = count_bits(as_columns(iter(example_input.splitlines())))
        assert counted[0] == {0: 5, 1: 7}

    def test_calculate_gamma_rate(self):
        bits = to_most_common_bits(
            count_bits(as_columns(iter(example_input.splitlines())))
        )
        assert bits == [1, 0, 1, 1, 0]
        assert 22 == to_number(bits)

    def test_epsilon_rate(self):
        bits = to_most_common_bits(
            count_bits(as_columns(iter(example_input.splitlines())))
        )
        assert bits == [1, 0, 1, 1, 0]
        epsilon_bits = as_epsilon(bits)
        assert epsilon_bits == [0, 1, 0, 0, 1]
        assert 9 == to_number(epsilon_bits)

    def test_solve_part_one(self):
        with open(puzzle_input_path, "r", newline="\n") as f:
            bits = to_most_common_bits(count_bits(as_columns(iter(f.readlines()))))
            gamma = to_number(bits)
            epsilon = to_number(as_epsilon(bits))
            power_consumption = gamma * epsilon
            assert power_consumption == 3847100

    def test_most_common_is_one_if_equal_number_of_bits(self):
        most_common_bits = to_most_common_bits(count_bits(as_columns(iter(["0", "1"]))))
        assert most_common_bits == [1]

    def test_most_common_bits_for_known_buggy_example(self):
        rows = ["11110", "11100", "11001"]
        counted_bits = count_bits(as_columns(iter(rows)))
        most_common_bits = to_most_common_bits(counted_bits)
        assert most_common_bits == [1, 1, 1, 0, 0]

    def test_counted_bits_always_has_zero_and_one(self):
        rows = ["10", "10", "10"]
        counted_bits = count_bits(as_columns(iter(rows)))
        assert {0: {0: 0, 1: 3}, 1: {0: 3, 1: 0}} == counted_bits

    def test_oxygen_rating(self):
        rating = get_o2_rating(example_input.splitlines())

        assert rating == 23

    def test_co2_scrubber_rating(self):
        rating = get_co2_scrubber_rating(example_input.splitlines())

        assert rating == 10

    def test_solve_part_two(self):
        with open(puzzle_input_path, "r", newline="\n") as f:
            lines = f.readlines()
            o2_rating = get_o2_rating(lines)
            co2_rating = get_co2_scrubber_rating(lines)

            assert o2_rating * co2_rating == 4105235
