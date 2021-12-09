from unittest import TestCase

example_input = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


def gather(signal_values: str):
    (unique_signal_patterns, four_digit_output_value) = signal_values.split(" | ")
    segments: list[str] = [
        "".join(sorted(s.strip())) for s in signal_values.split(" ") if s != "|"
    ]
    gathered = {
        "unique_signal_patterns": unique_signal_patterns,
        "four_digit_output_value": four_digit_output_value,
        "segments": {},
    }
    for segment in segments:
        if segment not in gathered["segments"]:
            match len(segment):
                case 2:
                    value = "1"
                case 4:
                    value = "4"
                case 3:
                    value = "7"
                case 7:
                    value = "8"
                case _:
                    value = "??"

            gathered["segments"][segment] = value

    return gathered


def draw(signal_wires: str):
    a = "a" if "a" in signal_wires else "."
    b = "b" if "b" in signal_wires else "."
    c = "c" if "c" in signal_wires else "."
    d = "d" if "d" in signal_wires else "."
    e = "e" if "e" in signal_wires else "."
    f = "f" if "f" in signal_wires else "."
    g = "g" if "g" in signal_wires else "."

    return f"""
    {a}{a}{a}{a}
   {b}    {c}
   {b}    {c}
    {d}{d}{d}{d}
   {e}    {f}
   {e}    {f}
    {g}{g}{g}{g}
"""


class TestDiscoverSignalValues(TestCase):
    def test_draw_numbers(self):
        assert (
            draw("cf")
            == """
    ....
   .    c
   .    c
    ....
   .    f
   .    f
    ....
"""
        )

        assert (
            draw("acf")
            == """
    aaaa
   .    c
   .    c
    ....
   .    f
   .    f
    ....
"""
        )

        assert (
            draw("bcdf")
            == """
    ....
   b    c
   b    c
    dddd
   .    f
   .    f
    ....
"""
        )
