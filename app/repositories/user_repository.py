from config.database import get_connection
import app.models.user

class UserRepository:
    def __init__(self):
        pass  # No need to store connection permanently

    def get_user_by_username(self, username):
        connection = get_connection()
        connection.row_factory = __import__('sqlite3').Row
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result:
            # Convert sqlite3.Row to dict for compatibility
            result = dict(result)
            return app.models.user.User(
                user_id=result.get('id'),
                username=result.get('username'),
                password=result.get('password'),
                role=result.get('role'),
                created_at=result.get('created_at'),
                assigned_cinema_id=result.get('assigned_cinema_id')
            )
        return None

    def get_all_users(self):
        connection = get_connection()
        connection.row_factory = __import__('sqlite3').Row
        cursor = connection.cursor()
        query = "SELECT * FROM users"
        cursor.execute(query)
        results = cursor.fetchall()

        users = []
        for result in results:
            result = dict(result)
            users.append(app.models.user.User(
                user_id=result.get('id'),
                username=result.get('username'),
                password=result.get('password'),
                role=result.get('role'),
                created_at=result.get('created_at'),
                assigned_cinema_id=result.get('assigned_cinema_id')
            ))
        
        cursor.close()
        connection.close()
        return users

    def add_user(self, user):
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO users (username, password, role, assigned_cinema_id) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (user.username, user.password, user.role, user.assigned_cinema_id))
        connection.commit()
        user_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return user_id

    def update_user(self, user):
        connection = get_connection()
        cursor = connection.cursor()
        query = "UPDATE users SET username = ?, password = ?, role = ?, assigned_cinema_id = ? WHERE id = ?"
        cursor.execute(query, (user.username, user.password, user.role, user.assigned_cinema_id, user.user_id))
        connection.commit()
        cursor.close()
        connection.close()

    def delete_user(self, user_id):
        connection = get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM users WHERE id = ?"
        cursor.execute(query, (user_id,))
        connection.commit()
        cursor.close()
        connection.close()