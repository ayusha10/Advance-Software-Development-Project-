import sqlite3

def get_connection():
    connection = sqlite3.connect("horizon_db.sqlite3")
    return connection
