from pathlib import Path
from unittest import TestCase

example_input = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


def parse_line(signal_pattern: str) -> (str, str):
    (unique_signal_patterns, four_digit_output_value) = signal_pattern.split(" | ")
    return unique_signal_patterns, four_digit_output_value


def as_lengths(entry: tuple[str, str]) -> tuple[list[int], list[int]]:
    return (
        [len(s) for s in entry[0].split(" ")],
        [len(s) for s in entry[1].split(" ")],
    )


def count_ones(signal_pattern_lengths: tuple[list[int], list[int]]) -> int:
    return sum(1 for length in signal_pattern_lengths[1] if length == 2)


def count_fours(signal_pattern_lengths: tuple[list[int], list[int]]) -> int:
    return sum(1 for length in signal_pattern_lengths[1] if length == 4)


def count_sevens(signal_pattern_lengths: tuple[list[int], list[int]]) -> int:
    return sum(1 for length in signal_pattern_lengths[1] if length == 3)


def count_eights(signal_pattern_lengths: tuple[list[int], list[int]]) -> int:
    return sum(1 for length in signal_pattern_lengths[1] if length == 7)


class TestSignals(TestCase):
    def test_letters_to_lengths(self):
        assert as_lengths(
            parse_line("a as asd asde asdef asdefg asdefgh | a as asd asde")
        ) == ([1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4])

    def test_can_find_ones(self):
        """one means only 2 signals on"""

        assert count_ones(as_lengths(parse_line("a AA a a a a | a AA aa"))) == 2

    def test_can_find_fours(self):
        """four means 4 signals on"""

        assert (
            count_fours(as_lengths(parse_line("a AAAA a a bbbb a | a AAAA AAAA AAAA")))
            == 3
        )

    def test_can_find_sevens(self):
        """seven means 3 signals on"""

        assert (
            count_sevens(as_lengths(parse_line("a AAA a acc bbbb a | a AAA AAA AAA")))
            == 3
        )

    def test_can_find_eights(self):
        """eight means 7 signals on"""

        assert (
            count_eights(
                as_lengths(parse_line("aaaaaaa AAA a acc ddddddd a | ddddddd ddddddd"))
            )
            == 2
        )

    def test_can_find_numbers_with_unique_signals_in_example_input(self):
        lines = [as_lengths(parse_line(line)) for line in example_input.splitlines()]
        total = 0

        for line in lines:
            for counter in [count_ones, count_fours, count_sevens, count_eights]:
                total += counter(line)

        assert total == 26

    def test_can_find_numbers_with_unique_signals_in_puzzle_input(self):
        puzzle_input_path = Path(__file__).parent / "./puzzle.input"
        with open(puzzle_input_path, "r", newline="\n") as f:
            lines = [as_lengths(parse_line(line.strip())) for line in f.readlines()]
            total = 0

            for line in lines:
                total += count_ones(line)
                total += count_fours(line)
                total += count_sevens(line)
                total += count_eights(line)

            assert total == 476
