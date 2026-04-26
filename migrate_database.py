import sqlite3
import os

def migrate_database():
    """
    Recreate the SQLite database with the updated schema that includes 'Customer' role.
    """
    db_file = "horizon_db.sqlite3"
    backup_file = "horizon_db.backup.sqlite3"
    
    try:
        # Backup existing database
        if os.path.exists(db_file):
            os.rename(db_file, backup_file)
            print(f"✓ Backed up existing database to {backup_file}")
        
        # Create new database with updated schema
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Read and execute the SQL schema
        with open("horizon_db.sql", "r") as sql_file:
            sql_script = sql_file.read()
            
        # Split by statement (simple splitting by semicolon)
        statements = sql_script.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement:
                cursor.execute(statement)
        
        conn.commit()
        print(f"✓ Created new database with updated schema")
        print("✓ Migration completed successfully!")
        print(f"✓ 'Customer' role is now supported")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"✗ Error during migration: {e}")
        # Restore backup if migration failed
        if os.path.exists(backup_file):
            os.rename(backup_file, db_file)
            print(f"✗ Restored backup from {backup_file}")

if __name__ == "__main__":
    migrate_database()
