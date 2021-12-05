from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Callable, Dict
from unittest import TestCase
from unittest.mock import Mock

example_input = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""


class Board:
    def __init__(self, board: str, win_listener: Callable[["Board", int], None]):
        self.win_listener = win_listener
        self.board: str = board
        self.numbers: Dict[str, tuple[int, int]] = {}
        self.marked_rows = {}
        self.marked_columns = {}

        rows = board.splitlines()
        self.column_win_length = len(rows)
        for y, row in enumerate(rows):
            x = -1  # cos not every enumerable column is a number
            for column in list(row.split(" ")):
                number = column.strip()
                if number:
                    x += 1
                    if number in self.numbers:
                        raise Exception(
                            f"number {number} is already on this board... \n\n{self.board} \n\n{self.numbers}"
                        )
                    self.numbers[number] = (x, y)

            self.row_win_length = x + 1

    def drawn(self, number: str) -> None:
        marked_positions = self.numbers.pop(number, None)
        if marked_positions is not None:
            (x, y) = marked_positions

            if y not in self.marked_rows:
                self.marked_rows[y] = []
            self.marked_rows[y].append(x)

            if x not in self.marked_columns:
                self.marked_columns[x] = []
            self.marked_columns[x].append(y)

        for marked_row in self.marked_rows.values():
            if len(marked_row) == self.row_win_length:
                self.win_listener(self, int(number))

        for marked_column in self.marked_columns.values():
            if len(marked_column) == self.column_win_length:
                self.win_listener(self, int(number))

    def unmarked_numbers(self):
        return list(self.numbers.keys())


@dataclass
class WinningGame:
    board: Board
    winning_number: int

    def final_score(self) -> int:
        unmarked_numbers = self.board.unmarked_numbers()
        sum_of_unmarked = sum([int(n) for n in unmarked_numbers])
        return sum_of_unmarked * self.winning_number


class Bingo:
    def __init__(self, drawn_numbers, boards: list[str]):
        self.boards = [Board(b, self.win) for b in boards]
        self.drawn_numbers = drawn_numbers
        self.winning_game: Optional[WinningGame] = None

    def win(self, board: Board, winning_number: int):
        if self.winning_game is None:
            self.winning_game = WinningGame(board, winning_number)

    @classmethod
    def parse(cls, subsystem_output: str) -> "Bingo":
        number_row, *boards = subsystem_output.split("\n\n")
        drawn_numbers = [n.strip() for n in number_row.split(",")]
        return Bingo(drawn_numbers, boards)

    def play(self):
        while self.winning_game is None:
            for number in self.drawn_numbers:
                for board in self.boards:
                    if self.winning_game is None:
                        board.drawn(number)
                    else:
                        break

        assert self.winning_game is not None
        return self.winning_game


class TestBingo(TestCase):
    def test_parse_bingo_game(self):
        game = Bingo.parse(example_input)
        assert game.drawn_numbers == [
            "7",
            "4",
            "9",
            "5",
            "11",
            "17",
            "23",
            "2",
            "0",
            "14",
            "21",
            "24",
            "10",
            "16",
            "13",
            "6",
            "15",
            "25",
            "12",
            "22",
            "18",
            "20",
            "8",
            "19",
            "3",
            "26",
            "1",
        ]
        assert len(game.boards) == 3

    def test_can_score_a_row_on_a_board(self):
        listener = Mock()

        board = Board(
            """ 1  2  3  4  5
 0  6  7  8  9
11 12 13 14 15""",
            listener,
        )

        assert board.numbers["0"] == (0, 1)
        assert board.numbers["1"] == (0, 0)
        assert board.numbers["2"] == (1, 0)
        assert board.numbers["3"] == (2, 0)
        assert board.numbers["4"] == (3, 0)
        assert board.numbers["5"] == (4, 0)

        board.drawn("1")
        assert "1" not in board.numbers

        board.drawn("2")
        assert "2" not in board.numbers

        board.drawn("3")
        assert "3" not in board.numbers

        board.drawn("4")
        assert "4" not in board.numbers

        board.drawn("5")
        assert "5" not in board.numbers

        assert board.marked_columns == {0: [0], 1: [0], 2: [0], 3: [0], 4: [0]}
        assert board.marked_rows == {0: [0, 1, 2, 3, 4]}

        listener.assert_called_with(board, 5)

    def test_can_score_a_column_on_a_board(self):
        listener = Mock()

        board = Board(
            """ 1  2  3  4  5
 0  6  7  8  9
11 12 13 14 15""",
            listener,
        )

        board.drawn("1")
        board.drawn("0")
        board.drawn("11")

        listener.assert_called_with(board, 11)

    def test_find_winner_in_the_example(self):
        game = Bingo.parse(example_input)
        winning_game = game.play()

        assert winning_game.winning_number == 24
        assert winning_game.final_score() == 4512

    def test_find_winner_in_puzzle_input(self):
        puzzle_input_path = Path(__file__).parent / "./puzzle.input"
        with open(puzzle_input_path, "r", newline="\n") as f:
            game = Bingo.parse(f.read())
            winning_game = game.play()

            assert winning_game.final_score() == 60368
