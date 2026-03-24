import os
from . import sqlite_setup

# Path to the SQLite database file
DB_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       'nine_mens_morris.db'))
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


# Drops all tables, all data deleted (for cleanup after tests mainly)
def drop_tables():
    conn = sqlite_setup.get_connection()
    try:
        cursor = conn.cursor()
        script_path = os.path.join(PROJECT_ROOT, "sql", "sqlite", "drop_db.sql")
        with open(script_path, 'r') as file:
            cursor.executescript(file.read())
        conn.commit()
    finally:
        conn.close()


if __name__ == '__main__':
    drop_tables()
    print("DB dropped.")
