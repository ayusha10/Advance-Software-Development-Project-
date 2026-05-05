import sqlite3
import os

def get_connection():
    db_path = os.getenv("DB_PATH", "horizon_db.sqlite3")
    connection = sqlite3.connect(db_path, timeout=30.0)
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA busy_timeout=30000")
    return connection
