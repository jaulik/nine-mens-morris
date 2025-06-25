import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..', 'src')))

from game.position import Position
from game.player import Player


class TestPosition(unittest.TestCase):
    def setUp(self):
        self.position = Position(4, [1, 3, 5, 7])

    def test_initial_vals(self):
        self.assertEqual(self.position.get_id(), 4)
        self.assertEqual(self.position.get_neighbors(), (1, 3, 5, 7))
        self.assertEqual(self.position.get_occupied_by(), None)

    def test_occupied_by(self):
        self.assertEqual(self.position.get_occupied_by(), None)
        player = Player("Anika", 11)
        self.position.set_occupied_by(player)
        self.assertEqual(self.position.get_occupied_by(), player)


if __name__ == "__main__":
    unittest.main()