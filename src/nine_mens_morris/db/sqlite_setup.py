import sqlite3
import os

# Path to the SQLite database file
DB_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       'nine_mens_morris.db'))
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# executes sqlite_schema.sql script
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    schema_path = os.path.join(PROJECT_ROOT, "sql", "sqlite", "create_schema.sql")
    with open(schema_path, 'r') as file:
        cursor.executescript(file.read())
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_tables()
    print("SQLite schema initialized.")
