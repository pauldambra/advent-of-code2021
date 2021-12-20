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
                    logging.debug(f"left hand side of explode is {left_number}")
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
                    logging.debug(f"so new left is {new_left}")
                    before_explode.next = new_left
                    new_left.previous = before_explode
                    before_explode = new_left
                    seeking_left = False
                    pointer = pointer.next
            else:
                if pointer.character == ",":
                    pointer = pointer.next

                logging.debug(f"seeking right. i see {pointer}")
                if pointer.character.isnumeric():
                    right_number = int(pointer.character)
                    logging.debug(f"right hand side of explode is {right_number}")
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
                    logging.debug(f"so new right is {new_right}")
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
                    logging.debug(f"now pointer is {pointer}")
                    nesting -= 2

                else:
                    pointer = pointer.next

    s = ""
    while pointer.previous:
        s += pointer.character
        pointer = pointer.previous

    return s[::-1]


class TestSnailNumbers(TestCase):
    def test_snailfish_numbers_can_be_parsed_from_strings(self):
        assert snailfish("[[[[[9,8],1],2],3],4]") == "[[[[0,9],2],3],4]"
        assert snailfish("[7,[6,[5,[4,[3,2]]]]]") == "[7,[6,[5,[7,0]]]]"
