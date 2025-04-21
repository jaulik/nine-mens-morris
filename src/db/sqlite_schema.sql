-- players
CREATE TABLE IF NOT EXISTS players (
  player_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  registered_at DATATIME DEFAULT (CURRENT_TIMESTAMP));

-- games
CREATE TABLE IF NOT EXISTS games (
  game_id INTEGER PRIMARY KEY AUTOINCREMENT,
  player1_id INTEGER NOT NULL REFERENCES players(player_id),
  player2_id INTEGER NOT NULL REFERENCES players(player_id),
  start_time DATATIME DEFAULT (CURRENT_TIMESTAMP),
  end_time DATATIME,
  winner_id INTEGER REFERENCES players(player_id),
  total_moves INTEGER NOT NULL);

-- statistics
CREATE TABLE IF NOT EXISTS statistics (
  player_id INTEGER PRIMARY KEY REFERENCES players(player_id),
  games_played INTEGER NOT NULL DEFAULT 0,
  games_won INTEGER NOT NULL DEFAULT 0,
  average_moves_to_win REAL);

-- trigger to recalculate statistics
CREATE TRIGGER IF NOT EXISTS trg_update_stats
AFTER INSERT ON games
BEGIN
  -- increase the amount of games played (both players)
  UPDATE statistics SET games_played = games_played + 1
  WHERE player_id IN (NEW.player1_id, NEW.player2_id);
  -- increase the amount of won games (winner)
  UPDATE statistics SET games_won = games_won + 1
  WHERE player_id = NEW.winner_id;
  -- recalculate avg moves to win (winner)
  UPDATE statistics SET average_moves_to_win =
    ((average_moves_to_win * (games_won - 1) + total_moves) / games_won)
    WHERE player_id = NEW.winner_id;
END;

-- trigger to insert player into statistics
CREATE TRIGGER IF NOT EXISTS trg_init_stats
AFTER INSERT ON players
BEGIN
  INSERT INTO statistics (player_id, games_played, games_won, average_moves_to_win)
  VALUES (NEW.player_id, 0, 0, NULL);
END;
