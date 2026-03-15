# Nine Men's Morris (CLI)

A command-line implementation of **Nine Men's Morris** with a small
**SQLite** backend for player/game statistics.

## Quickstart

### 1) Create & activate a virtual environment

**Linux / macOS / WSL**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install the package (editable)
From the repository root:
```bash
python -m pip install -U pip setuptools wheel
python -m pip install -e .
```

### 3) Run the game
```bash
python -m nine_mens_morris
```

---

## Run tests

### Unit tests (unittest)
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Coverage (optional)
```bash
python -m pip install coverage
coverage run -m unittest discover -s tests -p "test_*.py" -v
coverage report -m
```

---

## Project structure

### Python package (`src/nine_mens_morris`)
- `game/` — core game logic (board rules, turns, mills, win conditions)
  - `board.py` – Manages the 24-position board, placing/moving/removing pieces, and checking mill formations.
  - `game.py` – Coordinates the flow of the game, turn-taking, and win condition checks.
  - `player.py` – Represents a player (ID, name, pieces in hand / on board, mills).
  - `position.py` – Represents individual board positions (neighbors + occupancy).
  - `exceptions.py` – Custom exceptions for invalid moves/actions and bounds checks.
- `cli/` — command-line UI helpers
  - `game_runner.py` – CLI loop / input handling for game actions.
- `db/` — SQLite-backed persistence & stats
  - `sqlite_setup.py` – Creates tables using `sql/sqlite/create_schema.sql`.
  - `manage_db.py` – DB interface (players, games, statistics).
  - `clean_db.py` – Drops tables using `sql/sqlite/drop_db.sql`.

### SQL (`sql/`)
- `sql/sqlite/` — runtime SQLite scripts
  - `create_schema.sql` – Creates tables, triggers.
  - `drop_db.sql` – Drops all tables (dev/test helper).
- `sql/oracle/` — school project only (Oracle SQL/PLSQL)
  - Not used by the runtime application; included for demonstration.

---

## Notes / troubleshooting

- Always run commands **from the repository root** (where `pyproject.toml` is).
