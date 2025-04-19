
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

-- triggers
CREATE OR REPLACE TRIGGER statistics_trg
AFTER INSERT OR UPDATE ON games FOR EACH ROW
BEGIN
  update_statistics;
END;


CREATE OR REPLACE TRIGGER total_moves_trg
AFTER INSERT ON moves FOR EACH ROW
BEGIN
    UPDATE games SET total_moves = NVL(total_moves, 0) + 1 WHERE game_id = :NEW.game_id;
END;
/

-- cursor
DECLARE
  CURSOR c_player_durations IS
    SELECT p.name, COUNT(g.game_id) AS games, 
           ROUND(AVG((g.end_time - g.start_time) * 24 * 60), 2) AS avg_duration
    FROM players p JOIN games g ON p.player_id IN (g.player1_id, g.player2_id)
    WHERE g.end_time IS NOT NULL GROUP BY p.name
    HAVING COUNT(g.game_id) > 1 ORDER BY avg_duration ASC;

  rec c_player_durations%ROWTYPE;
BEGIN
  DBMS_OUTPUT.PUT_LINE('Average time by player:');
  FOR rec IN c_player_durations LOOP
    DBMS_OUTPUT.PUT_LINE(rec.name || ' (' || rec.games || ' games): ' || rec.avg_duration || ' min');
  END LOOP;
END;
/
