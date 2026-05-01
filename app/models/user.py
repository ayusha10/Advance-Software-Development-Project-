class User:
    def __init__(self, user_id, username, password, role, created_at=None, assigned_city_id=None):
        self.user_id = user_id
        self.username = username 
        self.password = password
        self.role = role
        self.created_at = created_at 
        self.assigned_city_id = assigned_city_id

    #getters methods 

    def get_user_id (self):
        return self.user_id 
    
    def get_username (self):
        return self.username
    
    def get_password(self):
        return self.password
    
    def get_role(self):
        return self.role 
    
    def get_created_at(self):
        return self.created_at

    def get_assigned_city_id(self):
        return self.assigned_city_id

 #ROLES 

    def can_book(self):
        return self.role == 'Customer'
    
    def is_admin(self):
        return self.role == 'Admin'
    
    def is_manager(self):
        return self.role == 'Manager'

