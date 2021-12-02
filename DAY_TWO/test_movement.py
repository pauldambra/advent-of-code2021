import dataclasses
from pathlib import Path
from typing import Iterator
from unittest import TestCase

puzzle_input_path = Path(__file__).parent / "./part1.input"

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

    @staticmethod
    def follow_instructions(instructions: Iterator[str]):
        position = Position()
        for instruction in iter(instructions):
            position = position.move(instruction)
        return position


@dataclasses.dataclass
class PartTwoPosition:
    horizontal: int = 0
    depth: int = 0
    aim: int = 0

    def move(self, instruction: str):
        parts = instruction.split(" ")
        if parts[0] == "forward":
            self.horizontal += int(parts[1])
            self.depth += int(parts[1]) * self.aim
        if parts[0] == "down":
            self.aim += int(parts[1])
        if parts[0] == "up":
            self.aim -= int(parts[1])

        return self

    @staticmethod
    def follow_instructions(instructions: Iterator[str]):
        position = PartTwoPosition()
        for instruction in iter(instructions):
            position = position.move(instruction)
        return position


class TestMovementPartTwo(TestCase):
    def test_going_forward(self):
        position = PartTwoPosition().move("forward 5")
        assert position.horizontal == 5
        assert position.depth == 0
        assert position.aim == 0

    def test_going_down(self):
        position = PartTwoPosition().move("forward 5").move("down 6")
        assert position.horizontal == 5
        assert position.depth == 0
        assert position.aim == 6

    def test_going_forward_and_down(self):
        position = PartTwoPosition().move("forward 5").move("down 5").move("forward 8")
        assert position.horizontal == 13
        assert position.depth == 40
        assert position.aim == 5

    def test_going_forward_and_up(self):
        position = (
            PartTwoPosition()
            .move("forward 5")
            .move("down 5")
            .move("forward 8")
            .move("up 3")
            .move("forward 2")
        )
        assert position.horizontal == 15
        assert position.depth == 44
        assert position.aim == 2

    def test_example(self):
        position = PartTwoPosition.follow_instructions(example.splitlines())
        assert position.horizontal == 15
        assert position.depth == 60
        assert position.horizontal * position.depth == 900

    def test_part_one(self):
        with open(puzzle_input_path, "r", newline="\n") as f:
            position = PartTwoPosition.follow_instructions(iter(f.readlines()))
            assert position.horizontal * position.depth == 1176514794


class TestMovementPartOne(TestCase):
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
        position = Position.follow_instructions(example.splitlines())

        assert position.horizontal * position.depth == 150

    def test_part_one(self):
        with open(puzzle_input_path, "r", newline="\n") as f:
            position = Position.follow_instructions(iter(f.readlines()))
            assert position.horizontal * position.depth == 1488669
