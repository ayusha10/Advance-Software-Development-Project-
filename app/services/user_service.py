from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()  # Must initialize this

    def authenticate_user(self, username, password):
        user = self.user_repo.get_user_by_username(username)
        if user and user.password == password:
            return user
        return None