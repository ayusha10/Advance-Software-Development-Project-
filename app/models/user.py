class User:
    def __init__(self, user_id, username, password, role, created_at):
        self.user_id = user_id
        self.username = username 
        self.password = password
        self.role = role
        self.created_at = created_at 

    #getters methods 

    def get_user_id (self):
        return self.id 
    
    def get_username (self):
        return self.username
    
    def get_password(self):
        return self.password
    
    def get_role(self):
        return self.role 
    
    def get_created_at(self):
        return self.created_at

 #ROLES 

    def can_book(self):
        return self.role == 'Customer'
    
    def is_admin(self):
        return self.role == 'Admin'
    
    def is_manager(self):
        return self.role == 'Manager'
    
    def is_staff(self):
        return self.role == 'Staff-Booking'
    
