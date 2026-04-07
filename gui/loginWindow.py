import tkinter as tk 
from tkinter import messagebox 

from app.controllers.auth_controller import AuthController
class LoginWindow:
    def __init__(self):
        self.controller = AuthController()
        self.root = tk.Tk()
        self.root.title("Horizon Cinema Login")
        self.root.geometry("300x200")

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Register as Customer", command=self.open_register_dialog).pack(pady=5)

        self.root.mainloop()

    def open_register_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Customer Registration")
        dialog.geometry("300x250")

        tk.Label(dialog, text="Username").pack(pady=5)
        u_entry = tk.Entry(dialog)
        u_entry.pack()

        tk.Label(dialog, text="Password").pack(pady=5)
        p_entry = tk.Entry(dialog, show="*")
        p_entry.pack()

        def register():
            username = u_entry.get()
            password = p_entry.get()
            if username and password:
                from app.models.user import User
                new_user = User(None, username, password, 'Customer', None)
                user_id = self.controller.register_user(new_user)
                if user_id:
                    messagebox.showinfo("Success", "Registration successful! Please login.")
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Username might already exist.")
            else:
                messagebox.showwarning("Warning", "All fields are required")

        tk.Button(dialog, text="Register", command=register).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.controller.login(username, password)

        if user:
            self.root.destroy()
            # Check Role
            if user.role == 'Admin':
                from gui.admin_panal import AdminPanel
                AdminPanel(user)
            elif user.role == 'Manager':
                from gui.manager_panal import ManagerPanel
                ManagerPanel(user)
            elif user.role == 'Customer':
                from gui.customer_panel import CustomerPanel
                CustomerPanel(user)
            else:
                messagebox.showinfo("Login Success", f"Welcome {user.username} ({user.role})")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")