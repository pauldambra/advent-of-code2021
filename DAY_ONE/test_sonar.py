from itertools import islice, tee
from pathlib import Path
from typing import Optional, Iterator
from unittest import TestCase

puzzle_input_path = Path(__file__).parent / "./part1.input"


def sliding_windows(sequence: Iterator, window_size: int = 3) -> list:
    iterables = tee(iter(sequence), window_size)
    window = zip(*(islice(t, n, None) for n, t in enumerate(iterables)))
    yield from window


def as_integers(ss: Iterator[str]) -> Iterator[int]:
    for s in ss:
        yield int(s)


def check_sonar_readings_for_increases(sonar_readings: Iterator[str]) -> int:
    previous: Optional[int] = None
    increases = 0
    for reading in [int(s) for s in sonar_readings]:
        if previous:
            if reading - previous > 0:
                increases += 1

        previous = reading
    return increases


example_sonar_readings = """199
200
208
210
200
207
240
269
260
263"""


class DayOne(TestCase):
    def test_example_sonar(self):
        increases = check_sonar_readings_for_increases(
            iter(example_sonar_readings.splitlines())
        )

        assert increases == 7

    def test_file_input(self):
        with open(puzzle_input_path, "r", newline="\n") as f:
            increases = check_sonar_readings_for_increases(iter(f.readlines()))

            assert increases == 1374

    def test_read_sequence_in_threes(self):
        sequence = [0, 1, 2, 3, 4, 5]
        assert [x for x in sliding_windows(sequence)] == [
            (0, 1, 2),
            (1, 2, 3),
            (2, 3, 4),
            (3, 4, 5),
        ]

    def test_sonar_example_sliding_window(self):
        increases = check_sonar_readings_for_increases(
            [
                sum(w)
                for w in sliding_windows(
                    as_integers(iter(example_sonar_readings.splitlines()))
                )
            ]
        )

        assert increases == 5

    def test_file_input_in_windows(self):
        with open(puzzle_input_path, "r", newline="\n") as f:
            increases = check_sonar_readings_for_increases(
                [sum(w) for w in sliding_windows(as_integers(iter(f.readlines())))]
            )

            assert increases == 1418
