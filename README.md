
# src

## game

This module contains the core game logic. It manages the rules, player actions, board state, and game phases.

Contents:

- `board.py` – Manages the 24-position board, placing/moving/removing pieces, and checking mill formations.
- `game.py` – Coordinates the flow of the game, turn-taking, and win condition checks.
- `player.py` – Represents a player with attributes like ID, name, pieces in hand and on board.
- `position.py` – Represents individual board positions, including their neighbors and occupancy.
- `exceptions.py` – Defines custom exception classes for invalid moves, illegal actions, or out-of-bounds positions.

## db

The db module contains all database-related functionality for working with the **SQLite** backend. It handles schema creation, data access for players/games/statistics, and provides helper scripts for development. 

Contents of the folder:

- `sqlite_setup.py`	- Establishing a SQLite connection and initializing the schema using the script `sql/sqlite/create_schema.sql`.
- `manage_db.py`	- Main database interface with functions to add players, start/end games, and retrieve game statistics.
- `clean_db.py` 	– Development helper script to drop all tables using the `sql/sqlite/drop_db.sql` script.
- `nine_mens_morris.db` – The SQLite database file (can be ignored in version control).

# SQL

## /sqlite - SQLite Runtime

The sql/sqlite directory contains two SQLite scripts. These scripts serve to setup or clean **SQLite database**.

Contents of folder:

 - `sqlite/create_schema.sql`		- Creates tables (players, games, statistics) and triggers.
 - `sqlite/drop_db.sql`			- Development helper, drops all tables.

## /oracle - school project only (Oracle SQL)

The sql/oracle directory contains a complete set of Oracle SQL scripts prepared for the Database Systems course project.
These scripts are not part of the runtime application, they are provided for demonstration of Oracle/PL‑SQL skills.

Contents of folder:

 - `oracle/create_tables.sql`		- Creates tables, seqences and defines referential intengrity constraints.
 - `oracle/insert_data.sql`		- Inserts sample data into tables.
 - `oracle/triggers_update.sql`		- Creates two triggers, procedure, cursor and recalculates statistics table.
 - `oracle/select.sql`			- Contains several select statements.
