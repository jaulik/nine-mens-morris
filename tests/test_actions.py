import unittest

from nine_mens_morris.game.board import Board
from nine_mens_morris.game.game import Game
from nine_mens_morris.game.game_state import GameState
from nine_mens_morris.game.player import Player
from nine_mens_morris.game.actions import Place, Move, Remove


class TestLegalActions(unittest.TestCase):
    def setUp(self):
        self.anika = Player("anika", 11)
        self.milan = Player("milan", 12)
        self.game = Game(self.anika, self.milan)

    def test_placing_returns_all_empty_positions(self):
        self.assertEqual(self.game.get_state(), GameState.PLACING)

        actions = self.game.legal_actions_for_current_player()

        self.assertEqual(len(actions), 24)
        self.assertTrue(all(isinstance(a, Place) for a in actions))
        positions = sorted(a.pos for a in actions)
        self.assertEqual(positions, list(range(24)))

    def test_move_only_neighbors_when_not_jumping(self):
        self.game.apply(Place(0))
        self.game.apply(Place(1))

        self.assertFalse(self.game.get_mills_formed())
        self.anika.set_pieces_in_hand(0)
        self.milan.set_pieces_in_hand(0)
        self.anika.set_pieces_on_board(4)
        self.milan.set_pieces_on_board(4)

        self.game.set_state(GameState.MOVING)
        self.assertEqual(self.game.get_current_player(), self.anika)

        actions = self.game.legal_actions_for_current_player()
        self.assertTrue(all(isinstance(a, Move) for a in actions))
        moves = {(a.pos_from, a.pos_to) for a in actions}
        self.assertIn((0, 9), moves)
        self.assertNotIn((0, 1), moves)
        self.assertEqual({(0,9)}, moves)

    def test_move_when_jumping(self):
        self.game.apply(Place(0))
        self.game.apply(Place(1))

        self.assertFalse(self.game.get_mills_formed())
        self.anika.set_pieces_in_hand(0)
        self.milan.set_pieces_in_hand(0)
        self.anika.set_pieces_on_board(3)
        self.milan.set_pieces_on_board(5)

        self.game.set_state(GameState.MOVING)
        self.assertEqual(self.game.get_current_player(), self.anika)

        actions = self.game.legal_actions_for_current_player()
        self.assertTrue(all(isinstance(a, Move) for a in actions))
        moves = {(a.pos_from, a.pos_to) for a in actions}
        possible_moves = {(0, pos) for pos in range(2, 24)}

        self.assertIn((0, 9), moves)
        self.assertIn((0, 23), moves)
        self.assertNotIn((0, 1), moves)
        self.assertEqual(possible_moves, moves)

    def test_remove_when_mill_formed(self):
        self.game.apply(Place(0)) # anika (p1)
        self.game.apply(Place(9)) # milan (p2)
        self.game.apply(Place(1)) # p1
        self.game.apply(Place(3)) # p2
        self.game.apply(Place(2)) # p1

        self.assertEqual(self.game.get_current_player(), self.anika)
        self.assertTrue(self.game.get_mills_formed())

        actions = self.game.legal_actions_for_current_player()
        self.assertTrue(all(isinstance(a, Remove) for a in actions))

        opponent_positions = {3,9}
        self.assertEqual({a.pos for a in actions}, opponent_positions)


if __name__ == "__main__":
    unittest.main()
