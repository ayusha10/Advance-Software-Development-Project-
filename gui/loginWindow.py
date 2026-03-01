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

        self.root.mainloop()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.controller.login(username, password)

        if user:
            messagebox.showinfo("Success", f"Welcome {user.get_role()}")
        else:
            messagebox.showerror("Error", "Invalid Credentials")