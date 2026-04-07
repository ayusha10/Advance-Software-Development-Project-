from app.services.user_service import UserService


class AuthController:
    def __init__ (self):
        self.user_service = UserService()

    def login(self, username, password):
        return self.user_service.authenticate_user(username, password)
    
    def register_user(self, user):
        return self.user_service.user_repo.add_user(user)