import sqlite3
import os

# Path to the SQLite database file
DB_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       'nine_mens_morris.db'))


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    return conn


# executes sqlite_schema.sql script
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    schema_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               '..', '..', 'sql', 'sqlite',
                                               'create_schema.sql'))
    with open(schema_path, 'r') as file:
        cursor.executescript(file.read())
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_tables()
    print("SQLite schema initialized.")
