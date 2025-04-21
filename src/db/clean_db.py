import os
import sqlite_setup

# Path to the SQLite database file
DB_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       'nine_mens_morris.db'))


# Drops all tables, all data deleted (for cleanup after tests mainly)
def drop_tables():
    conn = sqlite_setup.get_connection()
    cursor = conn.cursor()
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               '..', '..', 'sql',
                                               'drop_sqlite_db.sql'))
    with open(script_path, 'r') as file:
        cursor.executescript(file.read())
    conn.commit()
    conn.close()


if __name__ == '__main__':
    drop_tables()
    print("DB dropped.")
