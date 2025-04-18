-- insert testing data
INSERT INTO players (player_id, name) VALUES (seq_players_id.NEXTVAL, 'Julie');
INSERT INTO players (player_id, name) VALUES (seq_players_id.NEXTVAL, 'Rostislav');
INSERT INTO players (player_id, name) VALUES (seq_players_id.NEXTVAL, 'Petr');
INSERT INTO players (player_id, name) VALUES (seq_players_id.NEXTVAL, 'Miluse');

INSERT INTO games (game_id, player1_id, player2_id, start_time, end_time, winner, total_moves)
VALUES (seq_game_id.NEXTVAL, 1, 2, TO_DATE('2025-04-02 15:00', 'YYYY-MM-DD HH24:MI'),
        TO_DATE('2025-04-02 15:45', 'YYYY-MM-DD HH24:MI'), 1, 23);
INSERT INTO games (game_id, player1_id, player2_id, start_time, end_time, winner, total_moves)
VALUES (seq_game_id.NEXTVAL, 3, 4, TO_DATE('2025-04-02 16:00', 'YYYY-MM-DD HH24:MI'),
        TO_DATE('2025-04-02 16:45', 'YYYY-MM-DD HH24:MI'), 4, 28);
INSERT INTO games (game_id, player1_id, player2_id, start_time, end_time, winner, total_moves)
VALUES (seq_game_id.NEXTVAL, 1, 3, TO_DATE('2025-04-02 17:00', 'YYYY-MM-DD HH24:MI'),
        TO_DATE('2025-04-02 17:45', 'YYYY-MM-DD HH24:MI'), 3, 31);
INSERT INTO games (game_id, player1_id, player2_id, start_time, end_time, winner, total_moves)
VALUES (seq_game_id.NEXTVAL, 4, 2, TO_DATE('2025-04-02 18:00', 'YYYY-MM-DD HH24:MI'),
        TO_DATE('2025-04-02 18:45', 'YYYY-MM-DD HH24:MI'), 4, 18);

-- test data, few moves for each game
INSERT INTO moves (move_id, game_id, player_id, position_from, position_to)
VALUES (seq_moves_id.NEXTVAL, 1, 1, NULL, 'A1');
INSERT INTO moves (move_id, game_id, player_id, position_from, position_to)
VALUES (seq_moves_id.NEXTVAL, 1, 2, NULL, 'G1');
INSERT INTO moves (move_id, game_id, player_id, position_from, position_to)
VALUES (seq_moves_id.NEXTVAL, 1, 1, NULL, 'D1');

INSERT INTO moves (move_id, game_id, player_id, position_from, position_to)
VALUES (seq_moves_id.NEXTVAL, 2, 3, NULL, 'B2');
INSERT INTO moves (move_id, game_id, player_id, position_from, position_to)
VALUES (seq_moves_id.NEXTVAL, 2, 4, NULL, 'F2');
INSERT INTO moves (move_id, game_id, player_id, position_from, position_to)
VALUES (seq_moves_id.NEXTVAL, 2, 3, NULL, 'C3');

INSERT INTO moves (move_id, game_id, player_id, position_from, position_to)
VALUES (seq_moves_id.NEXTVAL, 3, 1, NULL, 'A4');
INSERT INTO moves (move_id, game_id, player_id, position_from, position_to)
VALUES (seq_moves_id.NEXTVAL, 3, 3, NULL, 'G4');
INSERT INTO moves (move_id, game_id, player_id, position_from, position_to)
VALUES (seq_moves_id.NEXTVAL, 3, 1, NULL, 'D1');

INSERT INTO moves (move_id, game_id, player_id, position_from, position_to)
VALUES (seq_moves_id.NEXTVAL, 4, 4, NULL, 'C1');
INSERT INTO moves (move_id, game_id, player_id, position_from, position_to)
VALUES (seq_moves_id.NEXTVAL, 4, 2, NULL, 'E1');
INSERT INTO moves (move_id, game_id, player_id, position_from, position_to)
VALUES (seq_moves_id.NEXTVAL, 4, 4, NULL, 'C4');
