import unittest

from nine_mens_morris.game.actions import Place, Remove, Move
from nine_mens_morris.game.board import Board
from nine_mens_morris.game.exceptions import PositionAlreadyOccupiedError

from nine_mens_morris.game.game_state import GameState
from nine_mens_morris.game.game import Game
from nine_mens_morris.game.player import Player


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
        self.game.apply(Place(0))
        self.game.apply(Place(1))
        self.assertEqual(self.anika.get_pieces_in_hand(), 8)
        self.assertEqual(self.anika.get_pieces_on_board(), 1)
        self.game.set_state(GameState.MOVING)
        self.assertEqual(self.game.get_action_generator().legal_actions_for(self.anika), [Move(0, 9)])
        self.assertEqual(self.game.get_current_player(), self.anika)

    def test_place_on_occupied_position(self):
        self.game.apply(Place(0))

        with self.assertRaises(ValueError):
            self.game.apply(Place(0))
        self.assertEqual(self.game.get_current_player(), self.milan)

    def test_transition_to_moving_state(self):
        for i in range(18):
            self.game.apply(Place(i))
        self.assertEqual(self.game.get_state(), GameState.MOVING)

    def test_jump(self):
        self.anika.set_pieces_on_board(3)
        self.anika.set_pieces_in_hand(0)
        self.milan.set_pieces_on_board(4)
        self.milan.set_pieces_in_hand(0)
        self.assertTrue(self.anika.can_jump())

        board = Board()
        board.place_piece(self.anika, 0)
        game = Game(self.anika, self.milan, board)
        game.set_state(GameState.JUMPING)

        game.apply(Move(0, 5))
        self.assertIsNone(game.get_player_on_position(0))
        self.assertEqual(game.get_player_on_position(5), self.anika)

    def test_remove(self):
        self.game.apply(Place(0))
        self.game.apply(Place(10))
        self.game.apply(Place(1))
        self.game.apply(Place(20))
        self.game.apply(Place(2))
        # anika created mill
        self.assertEqual(self.game.get_player_on_position(10), self.milan)
        self.game.apply(Remove(10))
        self.assertIsNone(self.game.get_player_on_position(10))

    def test_game_over_winner(self):
        self.anika.set_pieces_on_board(5)
        self.anika.set_pieces_in_hand(0)

        board = Board()
        board.place_piece(self.anika, 0)
        game = Game(self.anika, self.milan, board)

        self.milan.set_pieces_on_board(2)
        self.milan.set_pieces_in_hand(0)

        game.set_state(GameState.GAME_OVER)
        self.assertTrue(game.game_over())
        self.assertEqual(game.get_winner(), self.anika)


if __name__ == "__main__":
    unittest.main()