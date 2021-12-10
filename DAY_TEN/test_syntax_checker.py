from dataclasses import dataclass
from pathlib import Path
from queue import LifoQueue
from typing import Optional
from unittest import TestCase

chunk_delimiters = {"{": "}", "[": "]", "<": ">", "(": ")"}

valid_opening_characters = list(chunk_delimiters.keys())

readable_characters = valid_opening_characters + list(chunk_delimiters.values())

error_points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


@dataclass
class SyntaxCheckResult:
    is_valid: bool
    expected_character: Optional[str] = None
    illegal_character: Optional[str] = None


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
        return SyntaxCheckResult(
            is_valid=True,
            expected_character="incomplete",
            illegal_character="incomplete",
        )

    return SyntaxCheckResult(is_valid=True)


def syntax_check(lines: str) -> (list[SyntaxCheckResult], int):
    results = [is_valid_line(chunk) for chunk in lines.splitlines()]
    corrupt_lines = [chunk for chunk in results if not chunk.is_valid]
    score = sum([error_points[c.illegal_character] for c in corrupt_lines])
    return corrupt_lines, score


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
        corrupt_lines, score = syntax_check(example)
        assert len(corrupt_lines) == 5
        assert score == 26397

    def test_puzzle_input(self):
        puzzle_input_path = Path(__file__).parent / "./puzzle.input"
        with open(puzzle_input_path, "r", newline="\n") as f:
            _, score = syntax_check(f.read())
            assert score == 168417
