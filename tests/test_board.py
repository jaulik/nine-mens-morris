import unittest

from nine_mens_morris.game.board import Board
from nine_mens_morris.game.player import Player
from nine_mens_morris.game.exceptions import (
    PositionAlreadyOccupiedError,
    PositionOutOfBoundsError,
    InvalidMoveError,
    InvalidPieceRemovalError,
)


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.anika = Player("anika", 11)
        self.milan = Player("milan", 12)

    def test_place_piece(self):
        self.board.place_piece(self.anika, 0)
        self.assertEqual(self.board.occupied_by(0), self.anika)

    def test_move_piece(self):
        self.board.place_piece(self.anika, 0)
        self.board.place_piece(self.anika, 2)
        self.board.place_piece(self.anika, 4)
        self.board.place_piece(self.anika, 6)
        
        self.board.place_piece(self.milan, 1)
        self.board.place_piece(self.milan, 5)
        self.board.place_piece(self.milan, 7)
        self.board.place_piece(self.milan, 11)
        
        self.anika.set_pieces_on_board(4)
        self.anika.set_pieces_in_hand(0)
        self.milan.set_pieces_on_board(4)
        self.milan.set_pieces_in_hand(0)

        self.board.move_piece(0, 9, self.anika)
        self.assertIsNone(self.board.occupied_by(0))
        self.assertEqual(self.board.occupied_by(9), self.anika)

    def test_move_jump(self):
        self.milan.set_pieces_on_board(3)
        self.milan.set_pieces_in_hand(0)

        self.board.place_piece(self.milan, 21)
        self.assertTrue(self.milan.can_jump())

        self.board.move_piece(21, 12, self.milan)
        self.assertEqual(self.board.occupied_by(12), self.milan)
        self.assertIsNone(self.board.occupied_by(21))

    def test_remove_piece(self):
        self.board.place_piece(self.milan, 10)
        self.board.remove_piece(10, self.anika, self.milan)
        self.assertIsNone(self.board.occupied_by(10))

    def test_remove_piece_in_mill_not_allowed(self):
        self.board.place_piece(self.anika, 0)
        self.board.place_piece(self.anika, 1)
        self.board.place_piece(self.anika, 2)
        self.board.place_piece(self.anika, 3)
        with self.assertRaises(InvalidPieceRemovalError):
            self.board.remove_piece(0, self.milan, self.anika)

    def test_get_mill(self):
        self.board.place_piece(self.anika, 0)
        self.board.place_piece(self.anika, 1)
        self.board.place_piece(self.anika, 2)

        self.assertEqual(self.board.get_mill(0, self.anika), [0, 1, 2])
        self.assertIsNone(self.board.get_mill(3, self.anika))

    def test_remove_piece_in_mill_allowed_if_all_opponent_pieces_are_in_mills(self):
        self.board.place_piece(self.milan, 0)
        self.board.place_piece(self.milan, 1)
        self.board.place_piece(self.milan, 2)

        # Should be allowed because opponent has no stone outside of mills
        self.board.remove_piece(0, self.anika, self.milan)
        self.assertIsNone(self.board.occupied_by(0))

if __name__ == '__main__':
    unittest.main()