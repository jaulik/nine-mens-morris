PRAGMA foreign_keys = ON;

-- players
CREATE TABLE IF NOT EXISTS players (
  player_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  registered_at DATETIME DEFAULT (CURRENT_TIMESTAMP));

-- games
CREATE TABLE IF NOT EXISTS games (
  game_id INTEGER PRIMARY KEY AUTOINCREMENT,
  player1_id INTEGER NOT NULL REFERENCES players(player_id),
  player2_id INTEGER NOT NULL REFERENCES players(player_id),
  start_time DATETIME,
  end_time DATETIME,
  winner_id INTEGER REFERENCES players(player_id),
  total_moves INTEGER NOT NULL,
  CHECK (winner_id IS NULL OR winner_id = player1_id OR winner_id = player2_id));

-- statistics
CREATE TABLE IF NOT EXISTS statistics (
  player_id INTEGER PRIMARY KEY REFERENCES players(player_id),
  games_played INTEGER NOT NULL DEFAULT 0,
  games_won INTEGER NOT NULL DEFAULT 0,
  average_moves_to_win REAL);

-- trigger to recalculate statistics
CREATE TRIGGER IF NOT EXISTS trg_update_stats
AFTER UPDATE OF end_time ON games
WHEN NEW.end_time IS NOT NULL
BEGIN
  -- increase the amount of games played (both players)
  UPDATE statistics SET games_played = games_played + 1
  WHERE player_id IN (NEW.player1_id, NEW.player2_id);
  -- increase the amount of won games (winner)
  UPDATE statistics SET games_won = games_won + 1
  WHERE player_id = NEW.winner_id;
  -- recalculate avg moves to win (winner)
  UPDATE statistics SET average_moves_to_win =
    CASE
      WHEN average_moves_to_win IS NULL THEN NEW.total_moves
      ELSE ((average_moves_to_win * (games_won - 1) + NEW.total_moves) / games_won)
    END
    WHERE player_id = NEW.winner_id;
END;

-- trigger to insert player into statistics
CREATE TRIGGER IF NOT EXISTS trg_init_stats
AFTER INSERT ON players
BEGIN
  INSERT INTO statistics (player_id, games_played, games_won, average_moves_to_win)
  VALUES (NEW.player_id, 0, 0, NULL);
END;
