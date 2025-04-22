import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..', 'src')))

from db import sqlite_setup, clean_db, manage_db


def run_test_db():
    # clean database and setup new tables
    clean_db.drop_tables()
    sqlite_setup.create_tables()

    # add two players
    anika_id = manage_db.add_player("Anika")
    milan_id = manage_db.add_player("Milan")
    assert anika_id == 1 and milan_id == 2

    # start and end game
    game_id = manage_db.start_game(anika_id, milan_id)
    time.sleep(3)
    manage_db.end_game(anika_id, 25, game_id)

    anika_stats = manage_db.get_statistics(anika_id)
    milan_stats = manage_db.get_statistics(milan_id)

    assert anika_stats == {'player_id': 1,
                           'games_played': 1,
                           'games_won': 1,
                           'average_moves_to_win': 25.0,
                           'winrate': 100.0}
    assert milan_stats == {'player_id': 2,
                           'games_played': 1,
                           'games_won': 0,
                           'average_moves_to_win': None,
                           'winrate': 0.0}


if __name__ == "__main__":
    try:
        run_test_db()
    except Exception as e:
        print("Test failed!")
        raise e
    else:
        print("Test DB passed!")
    finally:
        clean_db.drop_tables()
