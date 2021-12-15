from dataclasses import dataclass
from typing import ClassVar, Optional
from unittest import TestCase

puzzle_input = """VOKKVSKKPSBVOOKVCFOV

PK -> P
BB -> V
SO -> O
OO -> V
PV -> O
CB -> H
FH -> F
SC -> F
KF -> C
VS -> O
VP -> V
FS -> K
SP -> C
FC -> N
CF -> C
BF -> V
FN -> K
NH -> F
OB -> F
SV -> H
BN -> N
OK -> K
NF -> S
OH -> S
FV -> B
OC -> F
VF -> V
HO -> H
PS -> N
NB -> N
NS -> B
OS -> P
CS -> S
CH -> N
PC -> N
BH -> F
HP -> P
HH -> V
BK -> H
HC -> B
NK -> S
SB -> C
NO -> K
SN -> H
VV -> N
ON -> P
VN -> H
VB -> P
BV -> O
CV -> N
HV -> C
SH -> C
KV -> F
BC -> O
OF -> P
NN -> C
KN -> F
CO -> C
HN -> P
PP -> V
FP -> O
CP -> S
FB -> F
CN -> S
VC -> C
PF -> F
PO -> B
KB -> H
HF -> P
SK -> P
SF -> H
VO -> N
HK -> C
HB -> C
OP -> B
SS -> V
NV -> O
KS -> N
PH -> H
KK -> B
HS -> S
PN -> F
OV -> S
PB -> S
NC -> B
BS -> N
KP -> C
FO -> B
FK -> N
BP -> C
NP -> C
KO -> C
VK -> K
FF -> C
VH -> H
CC -> F
BO -> S
KH -> B
CK -> K
KC -> C"""

example_input = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

PolymerTemplatePart = dict[int, tuple[str, int]]


@dataclass(frozen=True)
class PairInsertion:
    left: str
    right: str
    addition: str
    replacements: ClassVar[dict[tuple[int, str, int], tuple[int, str, int]]] = {}

    def process(self, template_pair: PolymerTemplatePart) -> PolymerTemplatePart:
        """

        e.g. starting with { 0: (N, 1), 1: (N, 2) }
        for rule NN -> NCN

        we'd end up with
            { 0: (N, 1), 1: (C, 2), 2: (N, 3) }

        subsequently

        anyone looking up (1, N, 2) needs to replace it with (2, N, 3)

        :param template_pair:
        :return:
        """
        assert len(template_pair) == 2
        left_matches = False
        right_matches = False
        first: Optional[tuple[int, str, int]] = None
        second: Optional[tuple[int, str, int]] = None

        for index, (key, (char, next_char_index)) in enumerate(template_pair.items()):
            if index == 0:
                left_matches = char == self.left
                first = (key, char, next_char_index)
            else:
                right_matches = char == self.right
                second = (key, char, next_char_index)

        assert first is not None
        assert second is not None

        first = PairInsertion.replacements.get(first, first)
        second = PairInsertion.replacements.get(second, second)

        insertion_result = {first[0]: (first[1], first[2])}
        if left_matches and right_matches:
            insertion_result[first[2]] = (self.addition, first[2] + 1)

            next_char_index = first[2] + 2 if second[2] != -1 else -1
            insertion_result[first[2] + 1] = (second[1], next_char_index)

            PairInsertion.replacements[second] = (
                first[2] + 1,
                second[1],
                next_char_index,
            )
        else:
            next_char_index = first[2] + 1 if second[2] != -1 else -1
            insertion_result[first[2]] = (second[1], next_char_index)

        return insertion_result


def parse(instructions: str) -> tuple[PolymerTemplatePart, list[PairInsertion]]:
    split = instructions.split("\n\n")
    template: list[str] = list(split[0])
    parsed_template = {}
    for index, character in enumerate(template):
        next_index = index + 1 if index + 1 < len(template) else -1
        parsed_template[index] = (character, next_index)

    instructions = split[1]
    parsed_instructions = []
    for instruction in instructions.splitlines():
        parts = instruction.split(" -> ")
        pair = list(parts[0])
        parsed_instructions.append(
            PairInsertion(left=pair[0], right=pair[1], addition=parts[1])
        )

    return parsed_template, parsed_instructions


def enumerate_pairs(polymer_template: PolymerTemplatePart) -> list[PolymerTemplatePart]:
    next_character = 0
    while next_character is not -1:
        pair = {}

        left = polymer_template[next_character]
        pair[next_character] = left
        next_character = left[1]

        if next_character is not -1:
            try:
                right = polymer_template[next_character]
            except KeyError:
                print(
                    f"key error while trying to read {next_character} from {polymer_template}"
                )
                raise

            pair[next_character] = right

            yield pair


def take_step(
    pair_insertions: list[PairInsertion], polymer_template: PolymerTemplatePart
):
    new_polymer_template = {}
    for pair in enumerate_pairs(polymer_template):
        result = {}
        for pair_insertion in pair_insertions:
            result = pair_insertion.process(pair)
            if len(result) == 3:
                break
        new_polymer_template.update(result)
    return new_polymer_template


class TestPolymers(TestCase):
    def test_can_parse_template(self):
        (polymer_template, _) = parse(example_input)
        assert polymer_template == {0: ("N", 1), 1: ("N", 2), 2: ("C", 3), 3: ("B", -1)}

    def test_can_enumerate_pairs_from_parsed(self):
        (polymer_template, _) = parse(example_input)
        pairs = [pair for pair in enumerate_pairs(polymer_template)]
        assert pairs == [
            {0: ("N", 1), 1: ("N", 2)},
            {1: ("N", 2), 2: ("C", 3)},
            {2: ("C", 3), 3: ("B", -1)},
        ]

    def test_can_parse_pair_insertions(self):
        (_, pair_insertions) = parse(example_input)
        assert pair_insertions == [
            PairInsertion("C", "H", "B"),
            PairInsertion("H", "H", "N"),
            PairInsertion("C", "B", "H"),
            PairInsertion("N", "H", "C"),
            PairInsertion("H", "B", "C"),
            PairInsertion("H", "C", "B"),
            PairInsertion("H", "N", "C"),
            PairInsertion("N", "N", "C"),
            PairInsertion("B", "H", "H"),
            PairInsertion("N", "C", "B"),
            PairInsertion("N", "B", "B"),
            PairInsertion("B", "N", "B"),
            PairInsertion("B", "B", "N"),
            PairInsertion("B", "C", "B"),
            PairInsertion("C", "C", "N"),
            PairInsertion("C", "N", "C"),
        ]

    def test_can_take_one_step(self):
        (polymer_template, pair_insertions) = parse(example_input)

        new_polymer_template = take_step(pair_insertions, polymer_template)

        assert new_polymer_template == {
            0: ("N", 1),
            1: ("C", 2),
            2: ("N", 3),
            3: ("B", 4),
            4: ("C", 5),
            5: ("H", 6),
            6: ("B", -1),
        }

    def test_can_take_ten_steps(self):
        (polymer_template, pair_insertions) = parse(example_input)

        for _ in range(10):
            polymer_template = take_step(pair_insertions, polymer_template)

        assert len(polymer_template) == 3073

    def test_can_count_chars_in_example_input(self):
        (polymer_template, pair_insertions) = parse(example_input)

        for _ in range(10):
            polymer_template = take_step(pair_insertions, polymer_template)

        counts = {}
        for (char, next) in polymer_template.values():
            if char not in counts:
                counts[char] = 0
            counts[char] += 1

        assert counts["B"] == 1749
        assert counts["C"] == 298
        assert counts["H"] == 161
        assert counts["N"] == 865

        max_letter = max(counts, key=counts.get)
        assert max_letter == "B"
        min_letter = min(counts, key=counts.get)
        assert min_letter == "H"

        assert counts[max_letter] - counts[min_letter] == 1588

    def test_can_count_chars_in_puzzle_input(self):
        (polymer_template, pair_insertions) = parse(puzzle_input)

        for _ in range(10):
            polymer_template = take_step(pair_insertions, polymer_template)

        counts = {}
        for (char, next) in polymer_template.values():
            if char not in counts:
                counts[char] = 0
            counts[char] += 1

        max_letter = max(counts, key=counts.get)
        min_letter = min(counts, key=counts.get)

        assert counts[max_letter] - counts[min_letter] == 3095
