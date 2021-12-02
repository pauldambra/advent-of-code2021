import dataclasses
from typing import Iterator
from unittest import TestCase

example = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""


@dataclasses.dataclass
class Position:
    horizontal: int = 0
    depth: int = 0

    def move(self, instruction: str):
        parts = instruction.split(" ")
        if parts[0] == "forward":
            self.horizontal += int(parts[1])
        if parts[0] == "down":
            self.depth += int(parts[1])
        if parts[0] == "up":
            self.depth -= int(parts[1])
        return self


def follow_instructions(instructions: Iterator[str]):
    position = Position()
    for instruction in iter(instructions):
        position = position.move(instruction)
    return position


class TestMovement(TestCase):
    def test_going_forward(self):
        position = Position().move("forward 5")
        assert position.horizontal == 5
        assert position.depth == 0

    def test_going_down(self):
        position = Position().move("forward 5").move("down 6")
        assert position.horizontal == 5
        assert position.depth == 6

    def test_going_up(self):
        position = Position().move("forward 5").move("down 6").move("up 11")
        assert position.horizontal == 5
        assert position.depth == -5

    def test_example(self):
        position = follow_instructions(example.splitlines())

        assert position.horizontal * position.depth == 150

    def test_part_one(self):
        with open("part1.input", "r", newline="\n") as f:
            position = follow_instructions(iter(f.readlines()))
            assert position.horizontal * position.depth == 1488669
