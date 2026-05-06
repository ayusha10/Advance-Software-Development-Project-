from app.repositories.user_repository import UserRepository
import logging

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()  # Must initialize this

    def authenticate_user(self, username, password):
        # Use logging at debug level instead of printing sensitive info to console.
        # Never log plaintext passwords.
        logger.debug("Authenticating user: %s", username)
        user = self.user_repo.get_user_by_username(username)
        if user:
            logger.debug("Found user; verifying password for user: %s", username)
            if user.password == password:
                logger.debug("Authentication successful for user: %s", username)
                return user
        else:
            logger.debug("User not found: %s", username)
        return None