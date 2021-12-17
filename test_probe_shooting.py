import dataclasses
from typing import Callable
from unittest import TestCase

puzzle_input = "target area: x=185..221, y=-122..-74"


def to_ranges(description: str) -> tuple[list[int, int], list[int, int]]:
    [x_desc, y_desc] = description[13:].split(", ")
    x_range_description = x_desc[2::].split("..")
    y_range_description = sorted(y_desc[2::].split(".."))
    x_range = [int(x) for x in x_range_description]
    y_range = [int(y) for y in y_range_description]
    # logging.debug(f"x_range: {x_range} and y_range: {y_range}")
    return x_range, y_range


def parse_target_is_passed(description: str) -> Callable[[tuple[int, int]], bool]:
    """
    negative y is down
    negative x is left
    :param description: looks like "x=-10..10, y=-10..10"
    :return:
    """
    (x_range, y_range) = to_ranges(description)

    def _is_passed(coord: tuple[int, int]) -> bool:
        is_passed_x = coord[0] > x_range[1]
        is_passed_y = coord[1] < y_range[0]
        # logging.debug(f"{coord[0]} > {x_range[1]}")
        # logging.debug(f"{coord[1]} < {y_range[0]}")
        # logging.debug(f"{coord} -> past x: {is_passed_x}, past y: {is_passed_y}")
        return is_passed_x or is_passed_y

    return _is_passed


def parse_target_is_within(description: str) -> Callable[[tuple[int, int]], bool]:
    """
    negative y is down
    negative x is left
    :param description: looks like "x=-10..10, y=--10..10"
    :return:
    """
    (x_range, y_range) = to_ranges(description)

    def _is_within(coord: tuple[int, int]) -> bool:
        is_within_x = x_range[0] <= coord[0] <= x_range[1]
        is_within_y = y_range[0] <= coord[1] <= y_range[1]
        # logging.debug(f"{x_range[0]} <= {coord[0]} <= {x_range[1]}")
        # logging.debug(f"{y_range[0]} <= {coord[1]} <= {y_range[1]}")
        # logging.debug(f"{coord} -> within x: {is_within_x}, within_y: {is_within_y}")
        return is_within_x and is_within_y

    return _is_within


@dataclasses.dataclass(frozen=True)
class Probe:
    x_velocity: int
    y_velocity: int
    position: tuple[int, int] = (0, 0)

    def step(self):
        """
        * The probe's x position increases by its x velocity.
        * The probe's y position increases by its y velocity.
        * Due to drag, the probe's x velocity changes by 1 toward the value 0; that is,
            it decreases by 1 if it is greater than 0, increases by 1 if it is less than 0,
            or does not change if it is already 0.
        * Due to gravity, the probe's y velocity decreases by 1.
        """
        return Probe(
            position=(
                self.position[0] + self.x_velocity,
                self.position[1] + self.y_velocity,
            ),
            x_velocity=self._approach_zero(self.x_velocity),
            y_velocity=self.y_velocity - 1,
        )

    @staticmethod
    def _approach_zero(x_velocity: int) -> int:
        if x_velocity == 0:
            return 0
        elif x_velocity > 0:
            return x_velocity - 1
        else:
            return x_velocity + 1


class TestProbeShooting(TestCase):
    """
    The probe launcher on your submarine can fire the probe with any integer velocity in the x (forward)
    and y (upward, or downward if negative) directions.

    For example, an initial x,y velocity like 0,10 would fire the probe straight up,
    while an initial velocity like 10,-1 would fire the probe forward at a slight downward angle.

    The probe's x,y position starts at 0,0. Then, it will follow some trajectory by moving in steps.
    On each step, these changes occur in the following order:

    * The probe's x position increases by its x velocity.
    * The probe's y position increases by its y velocity.
    * Due to drag, the probe's x velocity changes by 1 toward the value 0; that is,
        it decreases by 1 if it is greater than 0, increases by 1 if it is less than 0,
        or does not change if it is already 0.
    * Due to gravity, the probe's y velocity decreases by 1.
    """

    def test_probe_is_within_bounds(self):
        probe = (0, 0)
        is_within_target = parse_target_is_within("target area: x=-10..10, y=-10..10")
        assert isinstance(is_within_target, Callable)
        assert is_within_target(probe) is True

    def test_probe_is_past_bounds(self):
        probe = (0, 0)
        is_past_target = parse_target_is_passed("target area: x=7..10, y=-10..-5")
        assert isinstance(is_past_target, Callable)
        assert is_past_target(probe) is False
        assert is_past_target((10, -4)) is False
        assert is_past_target((10, -9)) is False
        assert is_past_target((11, -11)) is True
        assert is_past_target((9, 19)) is False
        assert is_past_target((11, 19)) is True

    def test_probe_coords_on_step(self):
        p = Probe(4, 5)
        assert p.position == (0, 0)
        assert p.x_velocity == 4
        assert p.y_velocity == 5
        p = p.step()
        assert p.x_velocity == 3
        assert p.y_velocity == 4
        assert p.position == (4, 5)

    def test_example_one(self):
        is_within_target = parse_target_is_within("target area: x=20..30, y=-10..-5")
        is_past_target = parse_target_is_passed("target area: x=20..30, y=-10..-5")
        p = Probe(7, 2)
        was_within_target = False
        step_count = 0
        max_height = 0
        expected_positions = [
            (0, 0),
            (7, 2),
            (13, 3),
            (18, 3),
            (22, 2),
            (25, 0),
            (27, -3),
            (28, -7),
        ]
        while was_within_target is False and not is_past_target(p.position):
            step_count += 1
            p = p.step()
            assert p.position == expected_positions[step_count]
            if p.position[1] > max_height:
                max_height = p.position[1]

            # logging.debug(f"probe is now {p}")
            if is_within_target(p.position):
                was_within_target = True

        assert step_count == 7
        assert was_within_target is True
        assert max_height == 3

    def test_find_max_height(self):
        is_within_target = parse_target_is_within("target area: x=20..30, y=-10..-5")
        is_past_target = parse_target_is_passed("target area: x=20..30, y=-10..-5")
        found_max_height = 0

        initial_velocity_on_target = []

        for x in range(0, 100):
            for y in range(-100, 100):
                p = Probe(x_velocity=x, y_velocity=y)
                was_within_target = False
                max_height = 0
                while was_within_target is False and not is_past_target(p.position):
                    p = p.step()
                    if p.position[1] > max_height:
                        max_height = p.position[1]

                    if is_within_target(p.position):
                        if max_height > found_max_height:
                            found_max_height = max_height
                        was_within_target = True
                        initial_velocity_on_target.append((x, y))

        assert found_max_height == 45
        assert len(initial_velocity_on_target) == 112

    def test_find_max_height_puzzle_input(self):
        is_within_target = parse_target_is_within(puzzle_input)
        is_past_target = parse_target_is_passed(puzzle_input)
        found_max_height = 0
        initial_velocity_on_target = []

        for x in range(0, 500):
            for y in range(-200, 500):
                p = Probe(x_velocity=x, y_velocity=y)
                was_within_target = False
                max_height = 0
                while was_within_target is False and not is_past_target(p.position):
                    p = p.step()
                    if p.position[1] > max_height:
                        max_height = p.position[1]

                    if is_within_target(p.position):
                        if max_height > found_max_height:
                            found_max_height = max_height
                        was_within_target = True
                        initial_velocity_on_target.append((x, y))

        assert found_max_height == 7381
        assert len(initial_velocity_on_target) == 3019
