import unittest
import os
import sys
import io
import contextlib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..', 'src')))

from src.game.game_state import GameState
from game.game import Game
from game.player import Player


class TestGame(unittest.TestCase):
    def setUp(self):
        self.anika = Player("anika", 11)
        self.milan = Player("milan", 12)
        self.game = Game(self.anika, self.milan)

    def test_initial(self):
        self.assertEqual(self.game.get_rounds(), 0)
        self.assertEqual(self.game.get_current_player(), self.anika)
        self.assertEqual(self.game.get_opposite_player(), self.milan)
        self.assertEqual(self.game.get_state(), GameState.PLACING)
        self.assertEqual(self.game.get_player1(), self.anika)
        self.assertEqual(self.game.get_player2(), self.milan)
        self.assertFalse(self.game.game_over())
        self.assertIsNone(self.game.get_winner())

    def test_switch(self):
        self.assertEqual(self.game.get_current_player(), self.anika)
        self.game.switch_current_player()
        self.assertEqual(self.game.get_current_player(), self.milan)

    def test_place_piece(self):
        self.game.play_round("place", 0)
        self.assertEqual(self.anika.get_pieces_in_hand(), 8)
        self.assertEqual(self.anika.get_pieces_on_board(), 1)
        self.assertEqual(self.game.get_all_possible_moves(self.anika), [1, 9])
        self.assertEqual(self.game.get_current_player(), self.milan)

    def test_place_on_occupied_position(self):
        self.game.play_round("place", 0)
        # redirect error msg to "black hole"
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            self.game.play_round("place", 0)
        self.assertEqual(self.game.get_current_player(), self.milan)

    def test_transition_to_moving_state(self):
        for i in range(18):
            self.game.play_round("place", i)
        self.assertEqual(self.game.get_state(), GameState.MOVING)

    def test_invalid_action(self):
        with self.assertRaises(ValueError):
            self.game.play_round("fly", 0)

    def test_jump(self):
        self.anika._Player__pieces_on_board = 3
        self.anika._Player__pieces_in_hand = 0
        self.milan._Player__pieces_on_board = 4
        self.milan._Player__pieces_in_hand = 0
        self.game._Game__state = GameState.JUMPING
        self.assertTrue(self.anika.can_jump())

        self.game._Game__board.place_piece(self.anika, 0)

        self.game.play_round("move", 0, 5)
        self.assertIsNone(self.game._Game__board.get_position(0).get_occupied_by())
        self.assertEqual(self.game._Game__board.get_position(5).get_occupied_by(), self.anika)

    def test_remove(self):
        self.game.play_round("place", 0)
        self.game.play_round("place", 10)
        self.game.play_round("place", 1)
        self.game.play_round("place", 20)
        self.game.play_round("place", 2)
        # anika created mill
        self.assertEqual(self.game._Game__board.get_position(10).get_occupied_by(), self.milan)
        self.game.play_round("remove", 10)
        self.assertIsNone(self.game._Game__board.get_position(10).get_occupied_by())

    def test_game_over_winner(self):
        self.anika._Player__pieces_in_hand = 0
        self.anika._Player__pieces_on_board = 5
        self.game._Game__board.place_piece(self.anika, 0)
        self.milan._Player__pieces_in_hand = 0
        self.milan._Player__pieces_on_board = 2
        self.game._Game__state = GameState.GAME_OVER
        self.assertTrue(self.game.game_over())
        self.assertEqual(self.game.get_winner(), self.anika)

    # TODO: test play + play_round

if __name__ == "__main__":
    unittest.main()