import logging
from typing import Optional
from unittest import TestCase


class thingy:
    def __init__(self, character: str):
        self.character: str = character
        self.previous: Optional["thingy"] = None
        self.next: Optional["thingy"] = None

    def __str__(self):
        return self.character


def pretty_print(thingy: thingy) -> str:
    logging.debug(f"pretty printing a thingy with previous {thingy.previous}")
    before = ""
    before_thingy = thingy
    while before_thingy.previous:
        before_thingy = before_thingy.previous
        before += before_thingy.character

    after = ""
    after_thingy = thingy
    while after_thingy.next:
        after_thingy = after_thingy.next
        after += after_thingy.character

    return f"\n{before[::-1]} * {thingy.character} * {after}"


def snailfish(snailfish_number: str) -> str:
    first, *rest = list(snailfish_number)
    previous = thingy(character=first)
    next = None
    for c in rest:
        next = thingy(c)
        previous.next = next
        next.previous = previous
        previous = next

    starting = next
    while starting.previous is not None:
        starting = starting.previous

    pointer: thingy = starting
    nesting = 0
    before_explode = None
    seeking_left = False
    while pointer.next:
        logging.debug("starting loop")
        logging.debug(pretty_print(pointer))

        if before_explode is None:
            if pointer.character == "[":
                nesting += 1
            elif pointer.character == "]":
                nesting -= 1
            pointer = pointer.next
            if nesting == 4:
                before_explode = pointer
                seeking_left = True
                pointer = pointer.next
        else:
            if seeking_left:
                if not pointer.character.isnumeric():
                    pointer = pointer.next
                else:
                    left_number = int(pointer.character)
                    logging.debug(pretty_print(pointer))
                    previous_number = None
                    number_seeker = pointer
                    while number_seeker.previous:
                        number_seeker = number_seeker.previous
                        if number_seeker.character.isnumeric():
                            previous_number = number_seeker.character
                            break

                    if previous_number:
                        left_number += int(previous_number)
                    else:
                        left_number = 0

                    new_left = thingy(str(left_number))
                    logging.debug(pretty_print(pointer))
                    before_explode.next = new_left
                    new_left.previous = before_explode
                    before_explode = new_left
                    seeking_left = False
                    pointer = pointer.next
            else:
                if pointer.character == ",":
                    pointer = pointer.next

                logging.debug(pretty_print(pointer))
                if pointer.character.isnumeric():
                    right_number = int(pointer.character)
                    logging.debug(pretty_print(pointer))
                    next_number = None
                    number_seeker = pointer
                    while number_seeker.next:
                        number_seeker = number_seeker.next
                        if number_seeker.character.isnumeric():
                            next_number = number_seeker.character
                            break

                    if next_number:
                        right_number += int(next_number)
                    else:
                        right_number = 0

                    new_right = thingy(str(right_number))
                    logging.debug(pretty_print(pointer))
                    comma = thingy(",")
                    before_explode.next = comma
                    comma.previous = before_explode
                    comma.next = new_right
                    new_right.previous = comma
                    new_right.next = number_seeker.next
                    before_explode = None
                    seeking_left = False

                    if number_seeker.next:
                        number_seeker.next.previous = new_right
                        pointer = new_right.next.next
                    else:
                        pointer = new_right
                    logging.debug(pretty_print(pointer))
                    nesting -= 2

                else:
                    pointer = pointer.next

    s = ""
    while pointer.previous:
        s += pointer.character
        pointer = pointer.previous

    return s[::-1]


class TestSnailNumbers(TestCase):
    def test_example_one(self):
        assert snailfish("[[[[[9,8],1],2],3],4]") == "[[[[0,9],2],3],4]"

    def test_example_two(self):
        assert snailfish("[7,[6,[5,[4,[3,2]]]]]") == "[7,[6,[5,[7,0]]]]"
