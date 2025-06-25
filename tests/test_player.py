import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..', 'src')))

from game.player import Player
from game.position import Position

class TestPlayer(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.anika = Player("Anika", 11)
        self.milan = Player("Milan", 12)
        self.anika2 = Player("Anika", 11)

    def test_initial_vals(self):
        self.assertEqual(self.anika.get_name(), "Anika")
        self.assertEqual(self.anika.get_id(), 11)
        self.assertEqual(self.anika.get_pieces_in_hand(), 9)
        self.assertEqual(self.anika.get_pieces_on_board(), 0)

    def test_equality_and_hash(self):
        self.assertTrue(self.anika == self.anika2)
        self.assertEqual(self.anika.__hash__(), self.anika2.__hash__())
        self.assertNotEqual(self.anika, self.milan)
        self.assertFalse(self.anika == Position(0, [1, 9]))

    def test_place_piece(self):
        self.anika.decrement_in_hand()
        self.anika.increment_on_board()
        self.assertEqual(self.anika.get_pieces_in_hand(), 8)
        self.assertEqual(self.anika.get_pieces_on_board(), 1)

    def test_jump_capability(self):
        for _ in range(9):
            self.assertFalse(self.milan.can_jump())
            self.milan.decrement_in_hand()
            self.milan.increment_on_board()
        
        for _ in range(6):
            self.milan.decrement_on_board()

        self.assertTrue(self.milan.can_jump())

    def test_mill(self):
        self.milan.add_mill([0, 1, 2])
        self.assertTrue(self.milan.has_had_mill([0, 1, 2]))
        self.assertFalse(self.milan.has_had_mill([3, 4, 5]))

if __name__ == "__main__":
    unittest.main()