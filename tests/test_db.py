import unittest
import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..', 'src')))

from db import sqlite_setup, clean_db, manage_db


class TestDbFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        clean_db.drop_tables()
        sqlite_setup.create_tables()

    @classmethod
    def tearDownClass(cls) -> None:
        clean_db.drop_tables()

    def test_add_get_players(self) -> None:
        anika_id = manage_db.add_player("Anika")
        milan_id = manage_db.add_player("Milan")
        self.assertEqual(anika_id, 1)
        self.assertEqual(milan_id, 2)

    def test_game(self) -> None:
        anika_id = manage_db.add_player("Anika")
        milan_id = manage_db.add_player("Milan")

        game_id = manage_db.start_game(anika_id, milan_id)
        time.sleep(1)
        manage_db.end_game(winner_id = anika_id, total_moves = 25, game_id = game_id)

        anika_stats = manage_db.get_statistics(anika_id)
        milan_stats = manage_db.get_statistics(milan_id)

        self.assertEqual(anika_stats['games_played'], 1)
        self.assertEqual(anika_stats['games_won'], 1)
        self.assertEqual(anika_stats['average_moves_to_win'], 25.0)
        self.assertEqual(anika_stats['winrate'], 100.0)

        self.assertEqual(milan_stats['games_played'], 1)
        self.assertEqual(milan_stats['games_won'], 0)
        self.assertEqual(milan_stats['average_moves_to_win'], None)
        self.assertEqual(milan_stats['winrate'], 0.0)

    def test_no_games_stats(self) -> None:
        random_nonexisting_id = 10
        angela_stats = manage_db.get_statistics(random_nonexisting_id)
        self.assertEqual(angela_stats['games_played'], 0)
        self.assertEqual(angela_stats['games_won'], 0)
        self.assertEqual(angela_stats['average_moves_to_win'], None)
        self.assertEqual(angela_stats['winrate'], None)

    def test_duplicate_player_names(self) -> None:
        id1 = manage_db.add_player("Eva")
        id2 = manage_db.add_player("Eva")
        self.assertNotEqual(id1, id2)

    def test_invalid_game_start(self) -> None:
        with self.assertRaises(Exception) as e:
            manage_db.start_game(999, 1000)
        self.assertEqual(str(e.exception), 'FOREIGN KEY constraint failed')
    
    def test_invalid_game_end(self) -> None:
        with self.assertRaises(Exception) as e:
            manage_db.end_game(winner_id=1, total_moves=20, game_id=999)
        self.assertEqual(str(e.exception), 'No game found with game_id=999')

    def test_stats_no_games(self) -> None:
        new_id = manage_db.add_player("NoGame")
        stats = manage_db.get_statistics(new_id)
        self.assertEqual(stats['games_played'], 0)
        self.assertEqual(stats['games_won'], 0)
        self.assertIsNone(stats['average_moves_to_win'], None)
        self.assertEqual(stats['winrate'], None)

    def test_multiple_games_stats(self) -> None:
        p1 = manage_db.add_player("Lena")
        p2 = manage_db.add_player("Otto")

        g1 = manage_db.start_game(p1, p2)
        time.sleep(1)
        manage_db.end_game(p1, 20, g1)

        g2 = manage_db.start_game(p1, p2)
        time.sleep(1)
        manage_db.end_game(p2, 30, g2)

        g3 = manage_db.start_game(p2, p1)
        time.sleep(1)
        manage_db.end_game(p1, 30, g3)

        g4 = manage_db.start_game(p2, p1)
        time.sleep(1)
        manage_db.end_game(p1, 25, g4)

        stats_p1 = manage_db.get_statistics(p1)
        self.assertEqual(stats_p1['games_played'], 4)
        self.assertEqual(stats_p1['games_won'], 3)
        self.assertEqual(stats_p1['average_moves_to_win'], 25.0)
        self.assertEqual(stats_p1['winrate'], 75.0)

        stats_p2 = manage_db.get_statistics(p2)
        self.assertEqual(stats_p2['games_played'], 4)
        self.assertEqual(stats_p2['games_won'], 1)
        self.assertEqual(stats_p2['average_moves_to_win'], 30.0)
        self.assertEqual(stats_p2['winrate'], 25.0)



if __name__ == "__main__":
    unittest.main()