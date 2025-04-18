
CREATE OR REPLACE PROCEDURE update_statistics IS
BEGIN
  DELETE FROM statistics;
  
  INSERT INTO statistics (player_id, games_played, games_won, average_moves_to_win)
  SELECT p.player_id, COUNT(g.game_id) AS games_played,
  SUM(CASE WHEN g.winner = p.player_id THEN 1 ELSE 0 END) AS games_won,
  ROUND(AVG(CASE WHEN g.winner = p.player_id THEN g.total_moves END), 2) AS average_moves_to_win

  FROM players p LEFT JOIN games g ON p.player_id IN (g.player1_id, g.player2_id) GROUP BY p.player_id;
END;
/

-- trigger
CREATE OR REPLACE TRIGGER statistics_trg
AFTER INSERT OR UPDATE ON games FOR EACH ROW
BEGIN
  update_statistics;
END;
