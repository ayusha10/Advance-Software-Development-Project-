from config.database import get_connection

def migrate_roles():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        print("Altering 'users' table to include 'Customer' role...")
        query = "ALTER TABLE users MODIFY COLUMN role ENUM('Admin', 'Manager', 'Booking-Staff', 'Customer') NOT NULL"
        cursor.execute(query)
        conn.commit()
        print("Success: 'Customer' role added to ENUM.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

if __name__ == "__main__":
    migrate_roles()
