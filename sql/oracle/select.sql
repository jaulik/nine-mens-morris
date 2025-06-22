-- ranking by winrate
SELECT
  RANK() OVER (ORDER BY s.games_won / NULLIF(s.games_played, 0) DESC) AS winrate_rank,
  p.player_id, p.name, s.games_played, s.games_won,
  ROUND(s.games_won / NULLIF(s.games_played, 0) * 100, 2) AS winrate_percent
FROM players p JOIN statistics s ON p.player_id = s.player_id WHERE s.games_played >= 1
ORDER BY winrate_percent DESC;

-- fastest win
SELECT g.game_id, p.name,
  ROUND((g.end_time - g.start_time) * 24 * 60, 1) as game_duration_min
FROM players p JOIN games g ON p.player_id = g.winner
WHERE ROUND((g.end_time - g.start_time) * 24 * 60, 1) = (SELECT MIN(ROUND((g2.end_time - g2.start_time) * 24 * 60, 1))
FROM games g2 WHERE g2.end_time IS NOT NULL);

-- less moves per game than average
SELECT p.name, ROUND(AVG(g.total_moves), 2) AS avg_moves_per_game
FROM players p JOIN games g ON player_id IN (player1_id, player2_id)
GROUP BY p.name HAVING AVG(g.total_moves) < (SELECT AVG(total_moves) FROM games)
ORDER BY avg_moves_per_game ASC;
