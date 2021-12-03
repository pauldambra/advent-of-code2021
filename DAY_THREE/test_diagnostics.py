from pathlib import Path
from typing import Iterator
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
        grouped[index] = {}
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


def as_epsilon(bits: list[int]) -> list[int]:
    return [1 if x == 0 else 0 for x in bits]


def to_number(bits):
    return int("".join([str(i) for i in bits]), 2)


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
