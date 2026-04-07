from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()  # Must initialize this

    def authenticate_user(self, username, password):
        print(f"Authenticating user: {username}")
        user = self.user_repo.get_user_by_username(username)
        if user:
            print(f"Found user. Comparing: '{user.password}' == '{password}'")
            if user.password == password:
                return user
        else:
            print("User not found.")
        return None