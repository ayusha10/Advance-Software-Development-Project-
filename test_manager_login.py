from app.repositories.user_repository import UserRepository

def test_login():
    repo = UserRepository()
    user = repo.get_user_by_username('manager26')
    if user:
        print(f"Found User: {user.username}, Role: {user.role}, Password: {user.password}, Assigned Cinema: {user.assigned_cinema_id}")
    else:
        print("User not found.")

if __name__ == "__main__":
    test_login()
