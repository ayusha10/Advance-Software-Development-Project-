from config.database import get_connection

def migrate():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Add assigned_cinema_id to users
        # Using IF NOT EXISTS if possible, but in standard MySQL we check columns
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN assigned_cinema_id INT NULL")
            cursor.execute("ALTER TABLE users ADD FOREIGN KEY (assigned_cinema_id) REFERENCES cinema(id) ON DELETE SET NULL")
            print("Successfully added assigned_cinema_id column.")
        except Exception as e:
            print(f"Column might already exist or error: {e}")

        # Assign manager26 to Cinema ID 1
        cursor.execute("UPDATE users SET assigned_cinema_id = 1 WHERE username = %s", ('manager26',))
        conn.commit()
        print("Updated manager26 with assigned_cinema_id = 1.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Migration error: {e}")

if __name__ == "__main__":
    migrate()
