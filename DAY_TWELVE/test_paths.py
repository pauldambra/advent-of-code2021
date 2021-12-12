from collections import Counter
from unittest import TestCase


class CaveSystem:
    def __init__(self, cave_description: str):
        self.paths = []
        self.cave_description = cave_description
        self.visited = {}
        self.links: dict[str, list[str]] = {}

        for p in self.cave_description.splitlines():
            start: str
            end: str
            start, end = p.split("-")
            start = start.strip()
            end = end.strip()
            if start not in self.links:
                self.links[start] = []
            if end not in self.links:
                self.links[end] = []

            self.links[start].append(end)
            self.links[end].append(start)

        self.paths = self.explore_caves("start", "end", [])

    def explore_caves(self, start: str, end: str, path: list[str]) -> list[list[str]]:
        path = path + [start]
        if start == end:
            return [path]

        paths = []
        for node in self.links.get(start, []):
            if node.isupper() or node not in path:
                new_paths = self.explore_caves(node, end, path)
                for new_path in new_paths:
                    paths.append(new_path)

        return paths


class CaveSystemPartTwo:
    def __init__(self, cave_description: str):
        self.paths = []
        self.cave_description = cave_description
        self.visited = {}
        self.links: dict[str, list[str]] = {}

        for p in self.cave_description.splitlines():
            start: str
            end: str
            start, end = p.split("-")
            start = start.strip()
            end = end.strip()
            if start not in self.links:
                self.links[start] = []
            if end not in self.links:
                self.links[end] = []

            self.links[start].append(end)
            self.links[end].append(start)

        self.paths = self.explore_caves("start", "end", [])

    def explore_caves(self, start: str, end: str, path: list[str]) -> list[list[str]]:
        path = path + [start]
        if start == end:
            return [path]

        paths = []
        for node in self.links.get(start, []):
            if self.can_visit(node, path):
                new_paths = self.explore_caves(node, end, path)
                for new_path in new_paths:
                    paths.append(new_path)

        return paths

    def can_visit(self, node, path):
        isupper = node.isupper()
        not_in_path = node not in path
        not_in_start_end_ = node not in ["start", "end"]
        nothing_in_path_twice = (
            max(Counter([p for p in path if p.islower()]).values()) < 2
        )
        can_visit = (
            isupper or not_in_path or (not_in_start_end_ and nothing_in_path_twice)
        )
        return can_visit


class TestPaths(TestCase):
    def test_single_path(self):
        cave_system = CaveSystem(
            """start-a
a-end"""
        )

        assert cave_system.paths == [["start", "a", "end"]]

    def test_two_paths(self):
        cave_system = CaveSystem(
            """start-a
            start-b
            b-end
a-end"""
        )

        assert cave_system.paths == [["start", "a", "end"], ["start", "b", "end"]]

    def test_three_paths(self):
        cave_system = CaveSystem(
            """start-a
            start-b
            b-end
            a-b
a-end"""
        )

        assert sorted(cave_system.paths) == sorted(
            [
                ["start", "a", "end"],
                ["start", "b", "end"],
                ["start", "a", "b", "end"],
                ["start", "b", "a", "end"],
            ]
        )

    def test_example_paths(self):
        cave_system = CaveSystem(
            """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
        )

        assert sorted(cave_system.paths) == sorted(
            [
                ["start", "A", "b", "A", "c", "A", "end"],
                ["start", "A", "b", "A", "end"],
                ["start", "A", "b", "end"],
                ["start", "A", "c", "A", "b", "A", "end"],
                ["start", "A", "c", "A", "b", "end"],
                ["start", "A", "c", "A", "end"],
                ["start", "A", "end"],
                ["start", "b", "A", "c", "A", "end"],
                ["start", "b", "A", "end"],
                ["start", "b", "end"],
            ]
        )

    def test_slightly_larger_example(self):
        cave_system = CaveSystem(
            """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""
        )
        assert len(cave_system.paths) == 19

    def test_even_larger_example(self):
        assert (
            len(
                CaveSystem(
                    """fs-end
                                                                                he-DX
                                                                                fs-he
                                                                                start-DX
                                                                                pj-DX
                                                                                end-zg
                                                                                zg-sl
                                                                                zg-pj
                                                                                pj-he
                                                                                RW-he
                                                                                fs-DX
                                                                                pj-RW
                                                                                zg-RW
                                                                                start-pj
                                                                                he-WI
                                                                                zg-he
                                                                                pj-fs
                                                                                start-RW"""
                ).paths
            )
            == 226
        )

    def test_puzzle_input(self):
        assert (
            len(
                CaveSystem(
                    """start-qs
                                                                        qs-jz
                                                                        start-lm
                                                                        qb-QV
                                                                        QV-dr
                                                                        QV-end
                                                                        ni-qb
                                                                        VH-jz
                                                                        qs-lm
                                                                        qb-end
                                                                        dr-fu
                                                                        jz-lm
                                                                        start-VH
                                                                        QV-jz
                                                                        VH-qs
                                                                        lm-dr
                                                                        dr-ni
                                                                        ni-jz
                                                                        lm-QV
                                                                        jz-dr
                                                                        ni-end
                                                                        VH-dr
                                                                        VH-ni
                                                                        qb-HE"""
                ).paths
            )
            == 5178
        )

    def test_example_paths_part_two(self):
        cave_system = CaveSystemPartTwo(
            """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
        )

        assert sorted(cave_system.paths) == sorted(
            [
                ["start", "A", "b", "A", "b", "A", "c", "A", "end"],
                ["start", "A", "b", "A", "b", "A", "end"],
                ["start", "A", "b", "A", "b", "end"],
                ["start", "A", "b", "A", "c", "A", "b", "A", "end"],
                ["start", "A", "b", "A", "c", "A", "b", "end"],
                ["start", "A", "b", "A", "c", "A", "c", "A", "end"],
                ["start", "A", "b", "A", "c", "A", "end"],
                ["start", "A", "b", "A", "end"],
                ["start", "A", "b", "d", "b", "A", "c", "A", "end"],
                ["start", "A", "b", "d", "b", "A", "end"],
                ["start", "A", "b", "d", "b", "end"],
                ["start", "A", "b", "end"],
                ["start", "A", "c", "A", "b", "A", "b", "A", "end"],
                ["start", "A", "c", "A", "b", "A", "b", "end"],
                ["start", "A", "c", "A", "b", "A", "c", "A", "end"],
                ["start", "A", "c", "A", "b", "A", "end"],
                ["start", "A", "c", "A", "b", "d", "b", "A", "end"],
                ["start", "A", "c", "A", "b", "d", "b", "end"],
                ["start", "A", "c", "A", "b", "end"],
                ["start", "A", "c", "A", "c", "A", "b", "A", "end"],
                ["start", "A", "c", "A", "c", "A", "b", "end"],
                ["start", "A", "c", "A", "c", "A", "end"],
                ["start", "A", "c", "A", "end"],
                ["start", "A", "end"],
                ["start", "b", "A", "b", "A", "c", "A", "end"],
                ["start", "b", "A", "b", "A", "end"],
                ["start", "b", "A", "b", "end"],
                ["start", "b", "A", "c", "A", "b", "A", "end"],
                ["start", "b", "A", "c", "A", "b", "end"],
                ["start", "b", "A", "c", "A", "c", "A", "end"],
                ["start", "b", "A", "c", "A", "end"],
                ["start", "b", "A", "end"],
                ["start", "b", "d", "b", "A", "c", "A", "end"],
                ["start", "b", "d", "b", "A", "end"],
                ["start", "b", "d", "b", "end"],
                ["start", "b", "end"],
            ]
        )

    def test_puzzle_input_paths_part_two(self):
        cave_system = CaveSystemPartTwo(
            """start-qs
                                                        qs-jz
                                                        start-lm
                                                        qb-QV
                                                        QV-dr
                                                        QV-end
                                                        ni-qb
                                                        VH-jz
                                                        qs-lm
                                                        qb-end
                                                        dr-fu
                                                        jz-lm
                                                        start-VH
                                                        QV-jz
                                                        VH-qs
                                                        lm-dr
                                                        dr-ni
                                                        ni-jz
                                                        lm-QV
                                                        jz-dr
                                                        ni-end
                                                        VH-dr
                                                        VH-ni
                                                        qb-HE"""
        )

        assert len(cave_system.paths) == 130094
