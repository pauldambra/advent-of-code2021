from dataclasses import dataclass, field
from functools import partial, update_wrapper
from queue import LifoQueue
from typing import Union
from unittest import TestCase


@dataclass(frozen=True)
class SnailFishNumber:
    x: Union[int, "SnailFishNumber"]
    y: Union[int, "SnailFishNumber"]
    parents: list[str] = field(default_factory=list, compare=False)

    def __post_init__(self):
        if isinstance(self.x, SnailFishNumber):
            self.x.parents.append(str(self))

        if isinstance(self.y, SnailFishNumber):
            self.y.parents.append(str(self))

    def __add__(self, other):
        return SnailFishNumber(self, other)

    @classmethod
    def parse(cls, description: str) -> "SnailFishNumber":
        init_queue = LifoQueue()
        binding_left = True
        for c in list(description):
            if c == "[":
                init_queue.put(SnailFishNumber)
            elif c == ",":
                binding_left = False
            elif c == "]":
                binding_left = True
            else:
                n = int(c)
                if binding_left:
                    constructor = init_queue.get()
                    bound_constructor = update_wrapper(
                        partial(constructor, x=n), constructor
                    )
                    init_queue.put(bound_constructor)
                else:
                    constructor = init_queue.get()
                    snailfish_number = constructor(y=n)
                    # if queue is not empty it is now the next init parameter of the next remaining init
                    if not init_queue.empty():
                        next_constructor = init_queue.get()
                        bound_next_constructor = update_wrapper(
                            partial(next_constructor, snailfish_number),
                            next_constructor,
                        )
                        init_queue.put(bound_next_constructor)
                        binding_left = True
                    else:
                        init_queue.put(snailfish_number)

        final_snailfish_number = init_queue.get()
        assert isinstance(final_snailfish_number, SnailFishNumber)

        final_snailfish_number

        return final_snailfish_number


class TestSnailNumbers(TestCase):
    def test_every_snailfish_number_is_a_pair(self):
        sfn = SnailFishNumber(1, 2)
        assert sfn == SnailFishNumber(1, 2)

    def test_part_of_a_snailfish_number_can_be_a_snailfish_number(self):
        sfn = SnailFishNumber(1, 2)
        assert SnailFishNumber(1, sfn) == SnailFishNumber(1, SnailFishNumber(1, 2))

    def test_can_add_numbers(self):
        """[1,2] + [[3,4],5] becomes [[1,2],[[3,4],5]]"""
        left = SnailFishNumber(1, 2)
        right = SnailFishNumber(SnailFishNumber(3, 4), 5)
        assert left + right == SnailFishNumber(
            SnailFishNumber(1, 2), SnailFishNumber(SnailFishNumber(3, 4), 5)
        )

    def test_snailfish_numbers_are_aware_of_their_nesting(self):
        left = SnailFishNumber(1, 2)
        assert left.parents == []
        nested = SnailFishNumber(3, 4)
        assert nested.parents == []
        SnailFishNumber(left, SnailFishNumber(1, nested))
        assert len(nested.parents) == 1

    def test_parse_the_simplest_snailfish_number(self):
        assert SnailFishNumber.parse("[1,2]") == SnailFishNumber(1, 2)

    def test_snailfish_numbers_can_be_parsed_from_strings(self):
        actual = SnailFishNumber(
            SnailFishNumber(
                SnailFishNumber(SnailFishNumber(SnailFishNumber(9, 8), 1), 2), 3
            ),
            4,
        )
        assert actual == SnailFishNumber.parse("[[[[0,9],2],3],4]")
