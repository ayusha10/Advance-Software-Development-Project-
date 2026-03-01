from config.database import get_connection
import app.models.user

class UserRepository:
    def __init__(self):
        pass  # No need to store connection permanently

    def get_user_by_username(self, username):
        # Get a new connection for each query
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result:
            return app.models.user.User(
                user_id=result['user_id'],
                username=result['username'],
                password=result['password'],
                role=result['role'],
                created_at=result['created_at']
            )
        return None