import logging
from pathlib import Path
from queue import SimpleQueue
from typing import Optional
from unittest import TestCase

hexa_to_binary = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def to_binary(hexadecimal: str) -> str:
    return "".join([hexa_to_binary[c] for c in list(hexadecimal)])


class Packet:
    LITERAL_TYPE = 4

    def __init__(self, source: str, starting_pointer: int = 0):
        self.version_sum = 0
        self.pointer = starting_pointer
        self.version = int(source[self.pointer : self.pointer + 3], 2)
        self.version_sum += self.version
        self.type_id = int(source[self.pointer + 3 : self.pointer + 6], 2)
        logging.debug(f"reading packet with type {self.type_id}")
        self.inner_packets: list[Packet] = []
        self.literal_value: Optional[int] = None
        if self.type_id == Packet.LITERAL_TYPE:
            self.pointer += 6
            binary_number = ""
            # read groups of five bits until one of them starts with 0 instead of 1
            group = None
            while group is None or group.startswith("1"):
                group = source[self.pointer : self.pointer + 5]
                binary_number += group[1:]
                self.pointer += 5

            self.literal_value = int(binary_number, 2)
            logging.debug(
                f"read literal value {self.literal_value} and ended at pointer position {self.pointer}"
            )
            return
        else:
            # it is an operator
            # an operator packet contains one or more sub packets
            self.length_type_id = int(
                source[starting_pointer + 6 : starting_pointer + 7], 2
            )
            if self.length_type_id == 0:
                bits_for_subpacket_length = 15
                self.subpacket_length = int(
                    source[
                        (starting_pointer + 7) : (
                            starting_pointer + 7 + bits_for_subpacket_length
                        )
                    ],
                    2,
                )

                self.pointer = starting_pointer + 7 + bits_for_subpacket_length
                # so the next `subpacket_length` bits contain one or more packets
                operator_ends_at = self.pointer + self.subpacket_length
                logging.debug(f"operator ends at {operator_ends_at}")
                while self.pointer < operator_ends_at - 1:
                    logging.debug(f"pointer is currently {self.pointer}")
                    self.inner_packets.append(Packet(source, self.pointer))
                    self.pointer = self.inner_packets[-1].pointer
            else:
                bits_for_subpacket_length = 11
                self.subpacket_length = int(
                    source[
                        starting_pointer
                        + 7 : (starting_pointer + 7 + bits_for_subpacket_length)
                    ],
                    2,
                )
                self.pointer = starting_pointer + 7 + bits_for_subpacket_length
                # so the operator contains `subpacket_length` number of packets
                for _ in range(self.subpacket_length):
                    logging.debug(f"pointer is currently {self.pointer}")
                    self.inner_packets.append(Packet(source, self.pointer))
                    self.pointer = self.inner_packets[-1].pointer

            if self.type_id == 0:
                self.literal_value = sum(
                    [
                        p.literal_value
                        for p in self.inner_packets
                        if p.literal_value is not None
                    ]
                )
                logging.debug(
                    f"read sum operator with literal value {self.literal_value}"
                )

            if self.type_id == 1:
                for p in [
                    ip for ip in self.inner_packets if ip.literal_value is not None
                ]:
                    if self.literal_value is None:
                        self.literal_value = p.literal_value
                    else:
                        self.literal_value *= p.literal_value
                logging.debug(
                    f"read product operator with literal value {self.literal_value}"
                )

            if self.type_id == 2:
                literal_values = [
                    ip.literal_value
                    for ip in self.inner_packets
                    if ip.literal_value is not None
                ]
                self.literal_value = (
                    min(literal_values) if len(literal_values) > 0 else None
                )

            if self.type_id == 3:
                literal_values = [
                    ip.literal_value
                    for ip in self.inner_packets
                    if ip.literal_value is not None
                ]
                self.literal_value = (
                    max(literal_values) if len(literal_values) > 0 else None
                )

            if self.type_id == 5:
                self.literal_value = (
                    1
                    if self.inner_packets[0].literal_value
                    > self.inner_packets[1].literal_value
                    else 0
                )

            if self.type_id == 6:
                self.literal_value = (
                    1
                    if self.inner_packets[0].literal_value
                    < self.inner_packets[1].literal_value
                    else 0
                )

            if self.type_id == 7:
                self.literal_value = (
                    1
                    if self.inner_packets[0].literal_value
                    == self.inner_packets[1].literal_value
                    else 0
                )

            q = SimpleQueue()
            for p in self.inner_packets:
                q.put(p)

            while not q.empty():
                current = q.get()
                self.version_sum += current.version
                for ip in current.inner_packets:
                    q.put(ip)

    @staticmethod
    def _next_multiple_of_four(start_pointer: int) -> int:
        n = start_pointer
        is_multiple_of_four = n % 4 == 0
        while not is_multiple_of_four:
            n += 1
            is_multiple_of_four = n % 4 == 0

        return n


class TestBITS(TestCase):
    def test_convert_hexadecimal_to_binary(self):
        assert to_binary("ABCDEF") == "101010111100110111101111"

    def test_convert_binary_to_number(self):
        assert int("1010", 2) == 10

    def test_read_packet_version(self):
        packets_source = to_binary("D2FE28")
        assert packets_source == "110100101111111000101000"
        assert Packet(packets_source).version == 6

    def test_read_packet_type_id(self):
        packets_source = to_binary("D2FE28")
        assert Packet(packets_source).type_id == 4

    def test_read_packet_value(self):
        packets_source = to_binary("D2FE28")
        packet = Packet(packets_source)
        assert packet.literal_value == 2021

    def test_can_read_operator_length_type_id(self):
        packets_source = to_binary("38006F45291200")
        assert (
            packets_source == "00111000000000000110111101000101001010010001001000000000"
        )
        packet = Packet(packets_source)
        assert packet.length_type_id == 0
        assert packet.subpacket_length == 27
        assert packet.pointer == 49
        assert packet.inner_packets[0].type_id == 4
        assert packet.inner_packets[0].literal_value == 10
        assert packet.inner_packets[1].version == 2
        assert packet.inner_packets[1].type_id == 4
        assert packet.inner_packets[1].literal_value == 20

    def test_can_read_operator_length_type_id_of_1(self):
        packets_source = to_binary("EE00D40C823060")
        assert (
            packets_source == "11101110000000001101010000001100100000100011000001100000"
        )
        packet = Packet(packets_source)
        assert packet.inner_packets[0].literal_value == 1
        assert packet.inner_packets[1].literal_value == 2
        assert packet.inner_packets[2].literal_value == 3

    def test_version_sum_example_one(self):
        packet = Packet(to_binary("8A004A801A8002F478"))
        assert packet.version_sum == 16

    def test_version_sum_example_two(self):
        packet = Packet(to_binary("620080001611562C8802118E34"))
        assert packet.version_sum == 12

    def test_version_sum_example_three(self):
        packet = Packet(to_binary("C0015000016115A2E0802F182340"))
        assert packet.version_sum == 23

    def test_version_sum_example_four(self):
        packet = Packet(to_binary("A0016C880162017C3686B18A3D4780"))
        assert packet.version_sum == 31

    def test_version_sum_puzzle_input(self):
        puzzle_input_path = Path(__file__).parent / "./puzzle.input"
        with open(puzzle_input_path, "r", newline="\n") as f:
            packet = Packet(to_binary(f.read()))
            assert packet.version_sum == 923

    def test_sum_operator(self):
        packet = Packet(to_binary("C200B40A82"))
        assert packet.literal_value == 3

    def test_product_operator(self):
        packet = Packet(to_binary("04005AC33890"))
        assert packet.literal_value == 54

    def test_min_operator(self):
        packet = Packet(to_binary("880086C3E88112"))
        assert packet.literal_value == 7

    def test_max_operator(self):
        packet = Packet(to_binary("CE00C43D881120"))
        assert packet.literal_value == 9

    def test_greater_than(self):
        packet = Packet(to_binary("F600BC2D8F"))
        assert packet.literal_value == 0

    def test_less_than(self):
        packet = Packet(to_binary("D8005AC2A8F0"))
        assert packet.literal_value == 1

    def test_equals(self):
        packet = Packet(to_binary("9C0141080250320F1802104A08"))
        assert packet.literal_value == 1

    def test_evaluate_puzzle_input(self):
        puzzle_input_path = Path(__file__).parent / "./puzzle.input"
        with open(puzzle_input_path, "r", newline="\n") as f:
            packet = Packet(to_binary(f.read()))
            assert packet.literal_value == 923
