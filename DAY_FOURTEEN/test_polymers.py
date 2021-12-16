import logging
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


def parse(instructions: str):
    parts = instructions.split("\n\n")
    return parts[0], {
        instruction[0]: f"{instruction[0][0]}{instruction[1]}"
        for instruction in [line.split(" -> ") for line in parts[1].splitlines()]
    }


cache: dict[str, str] = {}


def take_step(pair_insertions: dict[str, str], polymer_template: str):
    found: list[tuple[int, str]] = []
    for key in sorted(cache.keys(), key=len, reverse=True):
        index = polymer_template.find(key)
        if index > -1:
            found.append((index, key))

    # from start to end if none found
    if len(found) == 0:
        next_template = process_replacements(pair_insertions, polymer_template)
    else:
        # so go from start of string to first index in found doing replacements
        cached_sections = sorted(found, key=lambda x: x[0])
        logging.info(f"found cached sections: {cached_sections}")
        next_template = ""
        next_start = 0
        for section in cached_sections:
            found_index = section[0]
            cache_key = section[1]
            part = polymer_template[next_start : found_index + 1]
            replaced_part = process_replacements(pair_insertions, part)
            if next_start is not 0:
                replaced_part = replaced_part[1:]
            then = cache[cache_key]
            next_start = found_index + len(cache_key) - 1
            next_template += replaced_part + then

        if next_start != len(polymer_template):
            still_to_process = polymer_template[next_start:]
            final_piece = process_replacements(pair_insertions, still_to_process)
            next_template += final_piece[1:]

    new_template = next_template + polymer_template[-1]

    cache[polymer_template] = new_template
    return new_template


def process_replacements(pair_insertions: dict[str, str], haystack: str) -> str:
    replaced = ""
    for index in range(len(haystack)):
        if index + 1 < len(haystack):
            pair = haystack[index] + haystack[index + 1]
            to_insert = pair_insertions.get(pair, pair[0])
            replaced += to_insert
    return replaced


class TestPolymers(TestCase):
    def setup_method(self, method):
        cache.clear()

    def test_can_parse_template(self):
        (polymer_template, pair_insertions) = parse(example_input)
        assert polymer_template == "NNCB"
        assert pair_insertions == {
            "CH": "CB",
            "HH": "HN",
            "CB": "CH",
            "NH": "NC",
            "HB": "HC",
            "HC": "HB",
            "HN": "HC",
            "NN": "NC",
            "BH": "BH",
            "NC": "NB",
            "NB": "NB",
            "BN": "BB",
            "BB": "BN",
            "BC": "BB",
            "CC": "CN",
            "CN": "CC",
        }

    def test_can_take_one_step(self):
        (polymer_template, pair_insertions) = parse(example_input)

        next_template = take_step(pair_insertions, polymer_template)

        assert next_template == "NCNBCHB"

    def test_can_take_two_steps(self):
        (polymer_template, pair_insertions) = parse(example_input)

        next_template = take_step(pair_insertions, polymer_template)
        next_template = take_step(pair_insertions, next_template)

        assert next_template == "NBCCNBBBCBHCB"

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
        for char in list(polymer_template):
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
        for char in list(polymer_template):
            if char not in counts:
                counts[char] = 0
            counts[char] += 1

        max_letter = max(counts, key=counts.get)
        min_letter = min(counts, key=counts.get)

        assert counts[max_letter] - counts[min_letter] == 3095

    def test_copes_with_no_match(self):
        polymer_template = "ABDEFG"
        pair_instructions = {}
        assert take_step(pair_instructions, polymer_template) == "ABDEFG"

    def test_can_take_advantage_of_cache(self):
        polymer_template = "ABCDEFGHIJKLMNO"
        pair_instructions = {"AB": "AZ", "NO": "NZ"}
        cache["BCDEFGHIJKLMN"] = "replaced"
        assert take_step(pair_instructions, polymer_template) == "AZreplacedZO"

    def test_can_take_advantage_of_two_things_in_cache(self):
        # for template ABCDEFGHIJKLMNO
        # expecting ABCD to ABZC
        # and DEFG to replaced
        # and then GHIJ to HI (drop the G cos it is on the replaced section)
        # and then JKLM to also-replaced
        # and then MNO to NZO (drop the M cos it is on the replaced section)
        polymer_template = "ABCDEFGHIJKLMNO"
        pair_instructions = {"BC": "BZ", "NO": "NZ"}
        cache["DEFG"] = "replaced"
        cache["JKLM"] = "also-replaced"
        assert (
            take_step(pair_instructions, polymer_template)
            == "ABZCreplacedHIalso-replacedNZO"
        )

    # def test_can_count_chars_in_example_input_after_40_steps(self):
    #     (polymer_template, pair_insertions) = parse(example_input)
    #
    #     for step in range(40):
    #         logging.info(f"taking step {step + 1}")
    #         polymer_template = take_step(pair_insertions, polymer_template)
    #
    #     counts = {}
    #     for char in list(polymer_template):
    #         if char not in counts:
    #             counts[char] = 0
    #         counts[char] += 1
    #
    #     max_letter = max(counts, key=counts.get)
    #     assert max_letter == "B"
    #     min_letter = min(counts, key=counts.get)
    #     assert min_letter == "H"
    #
    #     assert counts[max_letter] - counts[min_letter] == 2188189693529
