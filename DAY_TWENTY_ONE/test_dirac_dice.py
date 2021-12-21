import dataclasses
import logging
from dataclasses import dataclass
from typing import Iterator
from unittest import TestCase

puzzle_input = """Player 1 starting position: 1
Player 2 starting position: 3"""

example_input = """Player 1 starting position: 4
Player 2 starting position: 8"""


@dataclass(frozen=True)
class Player:
    score: int
    position: int
    player_index: int

    def roll_for(self, player_index: int, roll: int) -> "Player":
        if player_index != self.player_index:
            logging.debug(
                f"this roll is not for player {self.player_index + 1}. Returning a clone"
            )
            return dataclasses.replace(self)
        else:
            new_position = track(starting_at=self.position, steps=roll)
            player = Player(
                score=self.score + new_position,
                position=new_position,
                player_index=self.player_index,
            )
            logging.debug(
                f"""
            player {self.player_index + 1} taking a turn
            starting with {self}
            having rolled {roll}
            ends at {player}
            """
            )
            return player

    def __str__(self):
        return f"score {self.score} at position {self.position}"


def roll_deterministic_dice() -> Iterator[int]:
    i = 0
    while True:
        i += 1
        if i > 100:
            i = 1

        logging.debug(f"die rolled {i}")
        yield i


def player_order_generator() -> Iterator[int]:
    next_player = 1
    while True:
        next_player = 0 if next_player == 1 else 1
        yield next_player


@dataclass(frozen=True)
class Game:
    players: tuple[Player, Player]
    die: Iterator[int] = dataclasses.field(
        default=roll_deterministic_dice(), compare=False
    )
    player_order: Iterator[int] = dataclasses.field(
        default=player_order_generator(), compare=False
    )

    def take_next_turn(self) -> "Game":
        roll_total = roll_three_times(self.die)

        player_index = next(self.player_order)

        return Game(
            (
                self.players[0].roll_for(player_index, roll_total),
                self.players[1].roll_for(player_index, roll_total),
            ),
            die=self.die,
            player_order=self.player_order,
        )

    @staticmethod
    def play_to(
        game: "Game", finishing_score: int
    ) -> tuple[int, tuple[Player, Player]]:
        number_of_turns: int = 0
        while (
            game.players[0].score < finishing_score
            and game.players[1].score < finishing_score
        ):
            number_of_turns += 3
            game = game.take_next_turn()

        return number_of_turns, game.players

    @staticmethod
    def parse(game_starting_description: str) -> "Game":
        (player_one, player_two) = [
            int(s[-1]) for s in game_starting_description.split("\n")
        ]
        return Game(
            players=(Player(0, player_one, 0), Player(0, player_two, 1)),
            die=roll_deterministic_dice(),
            player_order=player_order_generator(),
        )


def roll_three_times(die: Iterator[int]) -> int:
    return sum([next(die), next(die), next(die)])


def track(starting_at: int, steps: int) -> int:
    next_on_track = (starting_at + steps) % 10
    return 10 if next_on_track == 0 else next_on_track


class TestDiracDice(TestCase):
    def test_yield_one_to_a_hundred_and_then_wrap(self):
        expected = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
            53,
            54,
            55,
            56,
            57,
            58,
            59,
            60,
            61,
            62,
            63,
            64,
            65,
            66,
            67,
            68,
            69,
            70,
            71,
            72,
            73,
            74,
            75,
            76,
            77,
            78,
            79,
            80,
            81,
            82,
            83,
            84,
            85,
            86,
            87,
            88,
            89,
            90,
            91,
            92,
            93,
            94,
            95,
            96,
            97,
            98,
            99,
            100,
            1,
            2,
        ]

        dice = roll_deterministic_dice()
        for i in range(101):
            assert expected[i] == next(dice)

    def test_parse_starting_positions(self):
        game = Game.parse(example_input)
        assert game == Game((Player(0, 4, 0), Player(0, 8, 1)))

    def test_can_move_on_circular_track(self):
        assert track(starting_at=4, steps=2) == 6
        assert track(starting_at=2, steps=6) == 8
        assert track(starting_at=9, steps=1) == 10
        assert track(starting_at=10, steps=1) == 1
        assert track(starting_at=8, steps=4) == 2

    def test_can_roll_three_times_for_player_one(self):
        game = Game.parse(example_input)
        game = game.take_next_turn()
        assert game.players[0] == Player(10, 10, 0)

    def test_can_roll_three_times_for_player_two(self):
        game = Game.parse(example_input)
        # player two starts after player one
        game = game.take_next_turn()
        game = game.take_next_turn()
        assert game.players[1] == Player(3, 3, 1)

    def test_can_alternate_between_players(self):
        player_order = player_order_generator()
        assert next(player_order) == 0
        assert next(player_order) == 1
        assert next(player_order) == 0
        assert next(player_order) == 1

    def test_can_take_one_pair_of_goes(self):
        game = Game.parse(example_input)

        game = game.take_next_turn()
        game = game.take_next_turn()

        assert game.players == (Player(10, 10, 0), Player(3, 3, 1))

    def test_can_play_game_to_one_thousand(self):
        game = Game.parse(example_input)

        number_of_turns, players = Game.play_to(game, 1000)

        assert number_of_turns == 993
        assert min(players[0].score, players[1].score) == 745
        assert number_of_turns * min(players[0].score, players[1].score) == 739785

    def test_can_play_puzzle_input_game_to_one_thousand(self):
        game = Game.parse(puzzle_input)

        number_of_turns, players = Game.play_to(game, 1000)

        assert number_of_turns * min(players[0].score, players[1].score) == 897798
