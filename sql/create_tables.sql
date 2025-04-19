-- sequences for players, games, moves
CREATE SEQUENCE seq_players_id START WITH 1 NOCACHE;
CREATE SEQUENCE seq_game_id START WITH 1 NOCACHE;
CREATE SEQUENCE seq_moves_id START WITH 1 NOCACHE;

-- table for players
CREATE TABLE players (player_id integer PRIMARY KEY, name varchar2(20), registered_at date default SYSDATE);

-- table for games
CREATE TABLE games (game_id integer PRIMARY KEY,
                    player1_id integer REFERENCES players(player_id),
                    player2_id integer REFERENCES players(player_id),
                    start_time date, end_time date,
                    winner integer REFERENCES players(player_id),
                    total_moves integer);

-- table for moves
CREATE TABLE moves (move_id integer PRIMARY KEY,
                    game_id integer REFERENCES games(game_id),
                    player_id integer REFERENCES players(player_id),
                    position_from varchar2(20), position_to varchar2(20));

-- table for statistics
CREATE TABLE statistics (player_id integer PRIMARY KEY REFERENCES players(player_id),
                        games_played integer, games_won integer, average_moves_to_win integer);
