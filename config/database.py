import sqlite3

def get_connection():
    connection = sqlite3.connect("horizon_db.sqlite3", timeout=10.0)
    connection.execute("PRAGMA journal_mode=WAL")
    return connection
