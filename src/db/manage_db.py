import os
import sqlite_setup

# Path to the SQLite database file
DB_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       'nine_mens_morris.db'))


# Insert a new player into the players table and return their ID.
def add_player(name: str) -> int:
    conn = sqlite_setup.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
INSERT INTO players (name) VALUES (?)
""", (name,))
    player_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return player_id


# Start a new game and return its ID.
def start_game(player1_id: int, player2_id: int) -> int:
    conn = sqlite_setup.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
INSERT INTO games (player1_id, player2_id, start_time, total_moves)
VALUES (?, ?, CURRENT_TIMESTAMP, 0)
""", (player1_id, player2_id,))
    game_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return game_id


# End a game by updating the end time, winner, and total moves.
def end_game(player1_id, player2_id, winner_id: int, total_moves: int, game_id: int):
    conn = sqlite_setup.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
UPDATE games SET end_time = CURRENT_TIMESTAMP, winner_id = ?, total_moves = ?
WHERE game_id = ?
""", (winner_id, total_moves, game_id))
    conn.commit()
    conn.close()


# Retrieve statistics for a given player, including winrate.
def get_statistics(player_id: int) -> dict:
    conn = sqlite_setup.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
SELECT games_played, games_won, average_moves_to_win
FROM statistics WHERE player_id = ?
""", (player_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return {
            "player_id": player_id,
            "games_played": 0,
            "games_won": 0,
            "average_moves_to_win": None,
            "winrate": None
        }

    games_played, games_won, avg_moves = row
    return {
        "player_id": player_id,
        "games_played": games_played,
        "games_won": games_won,
        "average_moves_to_win": avg_moves,
        "winrate": round((games_won / games_played) * 100,
                         2) if games_played > 0 else None
    }
