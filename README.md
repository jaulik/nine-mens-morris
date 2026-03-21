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

## How the CLI is structured (Controllers + IO)

The runtime is split into three layers:

- **Game engine (`game/`)**: rules + state + legality (e.g. mills, legal moves, win conditions).
- **Controllers (`controllers/`)**: decide *which action to play* for the current player (human input, random bot, later minimax).
- **CLI (`cli/`)**: handles input/output and runs the main game loop.

At runtime:
1. `python -m nine_mens_morris` runs `src/nine_mens_morris/__main__.py`.
2. Two players are logged in/created in the SQLite database.
3. A `Game` is created, plus `ConsoleIO` and controllers.
4. `GameRunner` loops until game is over:
   - prints the board via `io.write(...)`
   - asks the current player's controller for an `Action`
   - calls `game.apply(action)`

This design makes it easy to plug in an AI opponent (controller) without changing the game engine.

**Switching opponents** (Human vs Random bot):
- By default, `__main__.py` starts **Human vs Human** (two `HumanController`s).

---

## Project structure

### Python package (`src/nine_mens_morris`)
- `game/` — core game logic (board rules, turns, mills, win conditions)
  - `board.py` – 24-position board rules (place/move/remove, mills).
  - `game.py` – game flow (turns, phases, applying actions, game over).
  - `action_generator.py` – generates legal actions from current state.
  - `player.py` – player state (ID, name, pieces in hand/on board, mills).
  - `position.py` – board positions (neighbors + occupancy).
  - `exceptions.py` – custom exceptions for invalid actions and bounds checks.
- `controllers/` — player “agents” (choose an action for current player)
  - `human_controller.py` – reads input via IO and returns an `Action`.
  - `random_controller.py` – chooses randomly from legal actions (baseline bot).
  - `base.py` – `Controller` Protocol.
- `cli/` — command-line UI helpers
  - `game_runner.py` – main CLI loop (delegates decisions to controllers).
  - `io.py` – `IO` Protocol (read/write abstraction).
  - `console_io.py` – console implementation using `input()` / `print()`.
- `db/` — SQLite-backed persistence & stats
  - `sqlite_setup.py` – creates tables using `sql/sqlite/create_schema.sql`.
  - `manage_db.py` – DB interface (players, games, statistics).
  - `clean_db.py` – drops tables using `sql/sqlite/drop_db.sql`.

### SQL (`sql/`)
- `sql/sqlite/` — runtime SQLite scripts
  - `create_schema.sql` – Creates tables, triggers.
  - `drop_db.sql` – Drops all tables (dev/test helper).
- `sql/oracle/` — school project only (Oracle SQL/PLSQL)
  - Not used by the runtime application; included for demonstration.

---

### Notes / troubleshooting

- Always run commands **from the repository root** (where `pyproject.toml` is).
