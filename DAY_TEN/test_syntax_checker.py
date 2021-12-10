import math
from dataclasses import dataclass
from pathlib import Path
from queue import LifoQueue
from typing import Optional
from unittest import TestCase

example = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

chunk_delimiters = {"{": "}", "[": "]", "<": ">", "(": ")"}

valid_opening_characters = list(chunk_delimiters.keys())

readable_characters = valid_opening_characters + list(chunk_delimiters.values())

error_points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

fix_points = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


@dataclass
class SyntaxCheckResult:
    is_valid: bool
    expected_character: Optional[str] = None
    illegal_character: Optional[str] = None
    needed_closing_characters: Optional[list[str]] = None


def is_valid_line(line: str) -> SyntaxCheckResult:
    chunk_opening_queue: LifoQueue = LifoQueue()
    for char in line:
        if char in readable_characters:
            if char in valid_opening_characters:
                chunk_opening_queue.put(char)
            else:
                expected_closing_character = chunk_delimiters.get(
                    chunk_opening_queue.get(), None
                )
                if char != expected_closing_character:
                    return SyntaxCheckResult(
                        is_valid=False,
                        expected_character=expected_closing_character,
                        illegal_character=char,
                    )

    if not chunk_opening_queue.empty():
        closers = list(
            reversed([chunk_delimiters[char] for char in chunk_opening_queue.queue])
        )

        return SyntaxCheckResult(
            is_valid=True,
            expected_character="incomplete",
            illegal_character="incomplete",
            needed_closing_characters=closers,
        )

    return SyntaxCheckResult(is_valid=True)


def syntax_check(
    lines: str,
) -> (list[SyntaxCheckResult], list[SyntaxCheckResult], int, list[int]):
    results = [is_valid_line(chunk) for chunk in lines.splitlines()]
    corrupt_lines = [chunk for chunk in results if not chunk.is_valid]
    score = sum([error_points[c.illegal_character] for c in corrupt_lines])
    incomplete_lines = [
        chunk for chunk in results if chunk.illegal_character == "incomplete"
    ]

    fix_scores = []
    for incomplete_line in incomplete_lines:
        fix_scores.append(0)
        for closer in incomplete_line.needed_closing_characters:
            fix_scores[-1] *= 5
            fix_scores[-1] += fix_points[closer]

    return incomplete_lines, corrupt_lines, score, fix_scores


class TestSyntaxChecker(TestCase):
    def test_a_single_chunk(self):
        line = "()"
        assert is_valid_line(line) == SyntaxCheckResult(is_valid=True)

    def test_an_incomplete_chunk(self):
        line = "("
        assert is_valid_line(line) == SyntaxCheckResult(
            is_valid=True,
            expected_character="incomplete",
            illegal_character="incomplete",
            needed_closing_characters=[")"],
        )

    def test_valid_chunks(self):
        chunks = [
            "([])",
            "{()()()}",
            "< ([{}]) >",
            "[ <> ({}){}[([]) <>]]",
            "(((((((((())))))))))",
        ]
        for chunk in chunks:
            print(chunk)
            assert is_valid_line(chunk) == SyntaxCheckResult(is_valid=True)

    def test_example_input(self):
        _, corrupt_lines, score, _ = syntax_check(example)
        assert len(corrupt_lines) == 5
        assert score == 26397

    def test_puzzle_input(self):
        puzzle_input_path = Path(__file__).parent / "./puzzle.input"
        with open(puzzle_input_path, "r", newline="\n") as f:
            _, _, score, _ = syntax_check(f.read())
            assert score == 168417

    def test_first_incomplete_line(self):
        incomplete_lines, _, _, fix_scores = syntax_check("[({(<(())[]>[[{[]{<()<>>")
        assert len(incomplete_lines) == 1
        assert incomplete_lines[0].needed_closing_characters == list("}}]])})]")

    def test_score_example_incomplete_lines(self):
        incomplete_lines, _, _, fix_scores = syntax_check(example)
        assert len(fix_scores) == 5

        assert fix_scores == [
            288957,
            5566,
            1480781,
            995444,
            294,
        ]

        assert sorted(fix_scores)[math.floor(len(fix_scores) / 2)] == 288957

    def test_score_puzzle_input_incomplete_lines(self):
        puzzle_input_path = Path(__file__).parent / "./puzzle.input"
        with open(puzzle_input_path, "r", newline="\n") as f:
            incomplete_lines, _, _, fix_scores = syntax_check(f.read())
            assert sorted(fix_scores)[len(fix_scores) // 2] == 2802519786
