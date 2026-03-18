import unittest

from nine_mens_morris.game.board import Board
from nine_mens_morris.game.game import Game
from nine_mens_morris.game.game_state import GameState
from nine_mens_morris.game.player import Player
from nine_mens_morris.game.actions import Place

class TestLegalActions(unittest.TestCase):
    def setUp(self):
        self.anika = Player("anika", 11)
        self.milan = Player("milan", 12)
        self.game = Game(self.anika, self.milan)
        self.board = Board()

    def test_placing_returns_all_empty_positions(self):
        self.assertEqual(self.game.get_state(), GameState.PLACING)

        actions = self.game.legal_actions_for_current_player()

        self.assertEqual(len(actions), 24)
        self.assertTrue(all(isinstance(a, Place) for a in actions))
        positions = sorted(a.pos for a in actions)
        self.assertEqual(positions, list(range(24)))

    # TODO: test move and remove


if __name__ == "__main__":
    unittest.main()