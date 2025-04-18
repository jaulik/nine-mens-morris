
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
  CURSOR c_games_avg IS
    SELECT game_id, ROUND((end_time - start_time) * 24 * 60, 1) AS duration_min FROM games
    WHERE end_time IS NOT NULL;
  rec c_games_avg%ROWTYPE;
BEGIN
  DBMS_OUTPUT.PUT_LINE('Doba her (min):');
  FOR rec IN c_games_avg LOOP
    DBMS_OUTPUT.PUT_LINE('Game ' || rec.game_id || ': ' || rec.duration_min || 'min');
  END LOOP;
END;
/
