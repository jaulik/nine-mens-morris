import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..', 'src')))

import src
from game.board import Board
from game.player import Player


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.anika = Player("anika", 11)
        self.milan = Player("milan", 12)

    def test_place_piece(self):
        self.board.place_piece(self.anika, 0)
        self.assertEqual(self.board.get_position(0).get_occupied_by(), self.anika)

        with self.assertRaises(src.game.exceptions.PositionAlreadyOccupiedError):
            self.board.place_piece(self.milan, 0)
        
        with self.assertRaises(src.game.exceptions.PositionOutOfBoundsError):
            self.board.place_piece(self.milan, 24)

    def test_move_piece(self):
        self.board.place_piece(self.anika, 0)
        self.board.place_piece(self.anika, 2)
        self.board.place_piece(self.anika, 4)
        self.board.place_piece(self.anika, 6)
        
        self.board.place_piece(self.milan, 1)
        self.board.place_piece(self.milan, 5)
        self.board.place_piece(self.milan, 7)
        self.board.place_piece(self.milan, 11)
        
        self.anika.__pieces_in_hand = 0
        self.anika.__pieces_on_board = 4
        self.milan.__pieces_in_hand = 0
        self.milan.__pieces_on_board = 4

        self.board.move_piece(0, 9, self.anika)
        self.assertIsNone(self.board.get_position(0).get_occupied_by())
        self.assertEqual(self.board.get_position(9).get_occupied_by(), self.anika)

        # Attempt move from wrong player
        with self.assertRaises(src.game.exceptions.InvalidMoveError):
            self.board.move_piece(1, 0, self.anika)

        # Attempt move to non-neighbor
        with self.assertRaises(src.game.exceptions.InvalidMoveError):
            self.board.move_piece(2, 12, self.anika)
        
        with self.assertRaises(src.game.exceptions.PositionOutOfBoundsError):
            self.board.move_piece(9, 24, self.anika)

        with self.assertRaises(src.game.exceptions.PositionAlreadyOccupiedError):
            self.board.move_piece(11, 6, self.milan)

    def test_move_jump(self):
        for _ in range(9):
            self.assertFalse(self.milan.can_jump())
            self.milan.decrement_in_hand()
            self.milan.increment_on_board()
        
        for _ in range(6):
            self.milan.decrement_on_board()

        self.board.place_piece(self.milan, 21)
        self.assertTrue(self.milan.can_jump())

        self.board.move_piece(21, 12, self.milan)
        self.assertEqual(self.board.get_position(12).get_occupied_by(), self.milan)
        self.assertIsNone(self.board.get_position(21).get_occupied_by())

    def test_remove_piece(self):
        with self.assertRaises(src.game.exceptions.PositionOutOfBoundsError):
            self.board.remove_piece(24, self.milan, self.anika)

        self.board.place_piece(self.milan, 10)
        # Invalid removal – not opponent
        with self.assertRaises(src.game.exceptions.InvalidPieceRemovalError):
            self.board.remove_piece(10, self.milan, self.anika)
        # Invalid removal - empty position
        with self.assertRaises(src.game.exceptions.InvalidPieceRemovalError):
            self.board.remove_piece(23, self.milan, self.anika)

        self.board.remove_piece(10, self.anika, self.milan)
        self.assertIsNone(self.board.get_position(10).get_occupied_by())


    def test_remove_piece_in_mill(self):
        self.board.place_piece(self.anika, 0)
        self.board.place_piece(self.anika, 1)
        self.board.place_piece(self.anika, 2)
        with self.assertRaises(src.game.exceptions.InvalidPieceRemovalError):
            self.board.remove_piece(0, self.milan, self.anika)

    def test_get_mill(self):
        self.board.place_piece(self.anika, 0)
        self.board.place_piece(self.anika, 1)
        self.board.place_piece(self.anika, 2)

        self.assertEqual(self.board.get_mill(0, self.anika), [0, 1, 2])
        self.assertIsNone(self.board.get_mill(3, self.anika))

if __name__ == '__main__':
    unittest.main()