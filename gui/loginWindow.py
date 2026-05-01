import tkinter as tk
from tkinter import ttk, messagebox 
from app.controllers.auth_controller import AuthController
from gui.theme import Theme
class LoginWindow:
    def __init__(self):
        self.controller = AuthController()
        self.root = tk.Tk()
        self.root.title("Horizon Cinema Login")
        self.root.geometry("400x450")
        
        # Apply Modern Theme
        Theme.apply(self.root)

        # Main Container with padding
        container = ttk.Frame(self.root, padding=40)
        container.pack(expand=True, fill='both')

        ttk.Label(container, text="HORIZON CINEMA", style="Header.TLabel").pack(fill='x', pady=(0, 30))

        ttk.Label(container, text="Username").pack(anchor='w')
        self.username_entry = ttk.Entry(container, font=Theme.FONT_MAIN)
        self.username_entry.pack(fill='x', pady=(5, 15))

        ttk.Label(container, text="Password").pack(anchor='w')
        self.password_entry = ttk.Entry(container, show="*", font=Theme.FONT_MAIN)
        self.password_entry.pack(fill='x', pady=(5, 30))

        ttk.Button(container, text="Login", command=self.login, style="Accent.TButton").pack(fill='x', pady=(0, 10))
        ttk.Button(container, text="Register as Customer", command=self.open_register_dialog).pack(fill='x')

        self.root.mainloop()

    def open_register_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Customer Registration")
        dialog.geometry("500x650")
        Theme.apply(dialog)

        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill='both')

        ttk.Label(container, text="Registration", style="Header.TLabel").pack(fill='x', pady=(0, 20))

        ttk.Label(container, text="Username").pack(anchor='w')
        u_entry = ttk.Entry(container, font=Theme.FONT_MAIN)
        u_entry.pack(fill='x', pady=(5, 15))

        ttk.Label(container, text="Password").pack(anchor='w')
        p_entry = ttk.Entry(container, show="*", font=Theme.FONT_MAIN)
        p_entry.pack(fill='x', pady=(5, 30))

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

        ttk.Button(container, text="Register", command=register, style="Success.TButton").pack(fill='x')

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