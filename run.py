from gui.loginWindow import LoginWindow
import sqlite3
import os

def initialize_database():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "horizon_db.sqlite3")
    sql_path = os.path.join(base_dir, "horizon_db.sql")
    
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    connection.close()
    
    if not tables:
        print("Database is empty. Initializing...")
        connection = sqlite3.connect(db_path)
        with open(sql_path, 'r') as f:
            sql_script = f.read()
        connection.executescript(sql_script)
        connection.close()
        print("Database initialized successfully.")
    else:
        print("Database already has tables.")

if __name__ == "__main__":
    initialize_database()
    LoginWindow()