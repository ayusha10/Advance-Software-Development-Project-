import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.admin_controller import AdminController

class AdminPanel:
    def __init__(self, user):
        self.user = user
        self.controller = AdminController()
        self.root = tk.Tk()
        self.root.title(f"Admin Dashboard - Welcome {user.username}")
        self.root.geometry("1000x700")

        # Layout
        self.create_widgets()
        
        self.root.mainloop()

    def create_widgets(self):
        # Header with Logout
        header_frame = tk.Frame(self.root)
        header_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(header_frame, text=f"Welcome, {self.user.username} (Admin)", font=("Arial", 12)).pack(side=tk.LEFT)
        tk.Button(header_frame, text="Logout", command=self.logout).pack(side=tk.RIGHT)

        # Create Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Create Frames for each Tab
        self.user_frame = ttk.Frame(self.notebook)
        self.cinema_frame = ttk.Frame(self.notebook)
        self.screen_frame = ttk.Frame(self.notebook)
        self.seat_frame = ttk.Frame(self.notebook)
        self.booking_frame = ttk.Frame(self.notebook)
        self.film_frame = ttk.Frame(self.notebook)
        self.city_frame = ttk.Frame(self.notebook)
        self.show_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.user_frame, text="User Management")
        self.notebook.add(self.cinema_frame, text="Cinema Management")
        self.notebook.add(self.screen_frame, text="Screen Management")
        self.notebook.add(self.seat_frame, text="Seat Management")
        self.notebook.add(self.booking_frame, text="Booking Management")
        self.notebook.add(self.film_frame, text="Film Management")
        self.notebook.add(self.city_frame, text="City Management")
        self.notebook.add(self.show_frame, text="Show Management")

        # Initialize each tab
        self.setup_user_tab()
        self.setup_cinema_tab()
        self.setup_screen_tab()
        self.setup_seat_tab()
        self.setup_booking_tab()
        self.setup_film_tab()
        self.setup_city_tab()
        self.setup_show_tab()

    def logout(self):
        self.root.destroy()
        from gui.loginWindow import LoginWindow
        LoginWindow()

    def setup_show_tab(self):
        tk.Label(self.show_frame, text="Show Management", font=("Arial", 16, "bold")).pack(pady=10)
        
        cols = ('ID', 'Film', 'Cinema', 'Screen', 'Time', 'Price')
        self.show_tree = ttk.Treeview(self.show_frame, columns=cols, show='headings')
        for col in cols:
            self.show_tree.heading(col, text=col)
            self.show_tree.column(col, width=120)
        self.show_tree.pack(expand=True, fill='both', padx=10, pady=10)

        btn_frame = tk.Frame(self.show_frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_shows).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Add Show", command=self.add_show_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Show", command=self.delete_show).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Edit Show", command=self.edit_show_dialog).pack(side=tk.LEFT, padx=5)

        self.refresh_shows()

    def refresh_shows(self):
        for item in self.show_tree.get_children():
            self.show_tree.delete(item)
        shows = self.controller.get_all_shows()
        for s in shows:
            self.show_tree.insert('', tk.END, values=(
                s.id, s.film_name, s.cinema_name, s.screen_number, s.show_time, s.base_price
            ))

    def add_show_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Schedule New Show")
        dialog.geometry("350x450")

        # Film Selection
        tk.Label(dialog, text="Select Film").pack(pady=5)
        films = self.controller.get_all_films()
        film_map = {f.name: f.id for f in films}
        film_combo = ttk.Combobox(dialog, values=list(film_map.keys()), state="readonly")
        film_combo.pack()

        # Screen Selection
        tk.Label(dialog, text="Select Screen").pack(pady=5)
        screens = self.controller.get_all_screens()
        # Admin can see all screens, so we show Cinema - Screen X
        screen_map = {f"{s.get_cinema_name()} - Screen {s.screen_number}": s.id for s in screens}
        screen_combo = ttk.Combobox(dialog, values=list(screen_map.keys()), state="readonly")
        screen_combo.pack()

        tk.Label(dialog, text="Show Date (YYYY-MM-DD)").pack(pady=5)
        date_entry = tk.Entry(dialog, width=30)
        date_entry.insert(0, "2026-04-10")
        date_entry.pack()

        tk.Label(dialog, text="Show Time (HH:MM:SS)").pack(pady=5)
        time_entry = tk.Entry(dialog, width=30)
        time_entry.insert(0, "18:00:00")
        time_entry.pack()

        tk.Label(dialog, text="Base Price").pack(pady=5)
        price_entry = tk.Entry(dialog, width=30)
        price_entry.insert(0, "10.00")
        price_entry.pack()

        def save_show():
            film_n = film_combo.get()
            screen_n = screen_combo.get()
            sdate = date_entry.get()
            stime = time_entry.get()
            price = price_entry.get()
            if film_n and screen_n and sdate and stime and price:
                from app.models.show import Show
                new_show = Show(None, film_map[film_n], screen_map[screen_n], sdate, stime, float(price))
                self.controller.add_show(new_show)
                self.refresh_shows()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "All fields are required")

        tk.Button(dialog, text="Save Show", command=save_show).pack(pady=20)

    def delete_show(self):
        selected = self.show_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a show first")
            return
        show_id = self.show_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", f"Delete show ID {show_id}?"):
            self.controller.delete_show(show_id)
            self.refresh_shows()

    def edit_show_dialog(self):
        selected = self.show_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a show first")
            return
        
        show_id = self.show_tree.item(selected[0])['values'][0]
        show = self.controller.get_show_by_id(show_id)
        if not show:
            messagebox.showerror("Error", "Show not found")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Show")
        dialog.geometry("350x450")

        tk.Label(dialog, text="Select Film").pack(pady=5)
        films = self.controller.get_all_films()
        film_map = {f.name: f.id for f in films}
        film_combo = ttk.Combobox(dialog, values=list(film_map.keys()), state="readonly")
        film_combo.pack()
        if show.film_name in film_map:
            film_combo.set(show.film_name)

        tk.Label(dialog, text="Select Screen").pack(pady=5)
        screens = self.controller.get_all_screens()
        screen_map = {f"{s.get_cinema_name()} - Screen {s.screen_number}": s.id for s in screens}
        screen_combo = ttk.Combobox(dialog, values=list(screen_map.keys()), state="readonly")
        screen_combo.pack()
        screen_label = f"{show.cinema_name} - Screen {show.screen_number}"
        if screen_label in screen_map:
            screen_combo.set(screen_label)

        tk.Label(dialog, text="Show Date (YYYY-MM-DD)").pack(pady=5)
        date_entry = tk.Entry(dialog, width=30)
        date_entry.insert(0, show.show_date)
        date_entry.pack()

        tk.Label(dialog, text="Show Time (HH:MM:SS)").pack(pady=5)
        time_entry = tk.Entry(dialog, width=30)
        time_entry.insert(0, show.show_time)
        time_entry.pack()

        tk.Label(dialog, text="Base Price").pack(pady=5)
        price_entry = tk.Entry(dialog, width=30)
        price_entry.insert(0, str(show.base_price))
        price_entry.pack()

        def update_show():
            film_n = film_combo.get()
            screen_n = screen_combo.get()
            sdate = date_entry.get()
            stime = time_entry.get()
            price = price_entry.get()
            if film_n and screen_n and sdate and stime and price:
                from app.models.show import Show
                updated_show = Show(show.id, film_map[film_n], screen_map[screen_n], sdate, stime, float(price))
                self.controller.update_show(updated_show)
                self.refresh_shows()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "All fields are required")

        tk.Button(dialog, text="Update Show", command=update_show).pack(pady=20)

    def setup_city_tab(self):
        tk.Label(self.city_frame, text="City Management", font=("Arial", 16, "bold")).pack(pady=10)
        
        cols = ('ID', 'Name')
        self.city_tree = ttk.Treeview(self.city_frame, columns=cols, show='headings')
        for col in cols:
            self.city_tree.heading(col, text=col)
            self.city_tree.column(col, width=300)
        self.city_tree.pack(expand=True, fill='both', padx=10, pady=10)

        btn_frame = tk.Frame(self.city_frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_cities).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Add City", command=self.add_city_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete City", command=self.delete_city).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Edit City", command=self.edit_city_dialog).pack(side=tk.LEFT, padx=5)

        self.refresh_cities()

    def refresh_cities(self):
        for item in self.city_tree.get_children():
            self.city_tree.delete(item)
        cities = self.controller.get_all_cities()
        for c in cities:
            self.city_tree.insert('', tk.END, values=(c.id, c.name))

    def add_city_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New City")
        dialog.geometry("300x150")

        tk.Label(dialog, text="City Name").pack(pady=5)
        name_entry = tk.Entry(dialog)
        name_entry.pack()

        def save_city():
            name = name_entry.get()
            if name:
                from app.models.city import City
                self.controller.add_city(name)
                self.refresh_cities()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "City name is required")

        tk.Button(dialog, text="Save", command=save_city).pack(pady=10)

    def delete_city(self):
        selected = self.city_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a city first")
            return
        city_id = self.city_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", f"Delete city ID {city_id}?"):
            self.controller.delete_city(city_id)
            self.refresh_cities()

    def edit_city_dialog(self):
        selected = self.city_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a city first")
            return
        
        city_id = self.city_tree.item(selected[0])['values'][0]
        current_name = self.city_tree.item(selected[0])['values'][1]

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit City")
        dialog.geometry("300x150")

        tk.Label(dialog, text="City Name").pack(pady=5)
        name_entry = tk.Entry(dialog)
        name_entry.insert(0, current_name)
        name_entry.pack()

        def update_city():
            name = name_entry.get()
            if name:
                self.controller.update_city(city_id, name)
                self.refresh_cities()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "City name is required")

        tk.Button(dialog, text="Update", command=update_city).pack(pady=10)


    def setup_film_tab(self):
        tk.Label(self.film_frame, text="Film Management", font=("Arial", 16, "bold")).pack(pady=10)
        
        cols = ('ID', 'Name', 'Genre', 'Rating', 'Duration')
        self.film_tree = ttk.Treeview(self.film_frame, columns=cols, show='headings')
        for col in cols:
            self.film_tree.heading(col, text=col)
            self.film_tree.column(col, width=120)
        self.film_tree.pack(expand=True, fill='both', padx=10, pady=10)

        btn_frame = tk.Frame(self.film_frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_films).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Add Film", command=self.add_film_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Film", command=self.delete_film).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Edit Film", command=self.edit_film_dialog).pack(side=tk.LEFT, padx=5)

        self.refresh_films()

    def refresh_films(self):
        for item in self.film_tree.get_children():
            self.film_tree.delete(item)
        films = self.controller.get_all_films()
        for f in films:
            self.film_tree.insert('', tk.END, values=(f.id, f.name, f.genre, f.age_rating, f.time_duration))

    def add_film_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Film")
        dialog.geometry("350x450")

        tk.Label(dialog, text="Name").pack(pady=5)
        name_entry = tk.Entry(dialog, width=30)
        name_entry.pack()

        tk.Label(dialog, text="Genre").pack(pady=5)
        genre_entry = tk.Entry(dialog, width=30)
        genre_entry.pack()

        tk.Label(dialog, text="Age Rating").pack(pady=5)
        rating_entry = tk.Entry(dialog, width=30)
        rating_entry.pack()

        tk.Label(dialog, text="Duration (mins)").pack(pady=5)
        dur_entry = tk.Entry(dialog, width=30)
        dur_entry.pack()

        tk.Label(dialog, text="Description").pack(pady=5)
        desc_text = tk.Text(dialog, height=4, width=30)
        desc_text.pack()

        def save_film():
            name = name_entry.get()
            genre = genre_entry.get()
            rating = rating_entry.get()
            dur = dur_entry.get()
            desc = desc_text.get("1.0", tk.END).strip()
            if name and genre and dur and rating:
                try:
                    from app.models.film import Film
                    new_film = Film(None, name, genre, rating, desc, int(dur))
                    self.controller.add_film(new_film)
                    self.refresh_films()
                    dialog.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Duration must be an integer (e.g. 120)")
            else:
                messagebox.showwarning("Warning", "All fields except Description are required")

        tk.Button(dialog, text="Save", command=save_film).pack(pady=20)

    def delete_film(self):
        selected = self.film_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a film first")
            return
        film_id = self.film_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", f"Delete film ID {film_id}?"):
            self.controller.delete_film(film_id)
            self.refresh_films()

    def edit_film_dialog(self):
        selected = self.film_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a film first")
            return
        
        film_id = self.film_tree.item(selected[0])['values'][0]
        
        # We need the full film object because tree doesn't have description.
        # However, the controller might not have a get_film_by_id. Let's see.
        # As an alternative, we'll try to find it in get_all_films().
        films = self.controller.get_all_films()
        film = next((f for f in films if f.id == film_id), None)
        
        if not film:
            messagebox.showerror("Error", "Film not found")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Film")
        dialog.geometry("350x450")

        tk.Label(dialog, text="Name").pack(pady=5)
        name_entry = tk.Entry(dialog, width=30)
        name_entry.insert(0, film.name)
        name_entry.pack()

        tk.Label(dialog, text="Genre").pack(pady=5)
        genre_entry = tk.Entry(dialog, width=30)
        genre_entry.insert(0, film.genre)
        genre_entry.pack()

        tk.Label(dialog, text="Age Rating").pack(pady=5)
        rating_entry = tk.Entry(dialog, width=30)
        rating_entry.insert(0, film.age_rating)
        rating_entry.pack()

        tk.Label(dialog, text="Duration (mins)").pack(pady=5)
        dur_entry = tk.Entry(dialog, width=30)
        dur_entry.insert(0, str(film.time_duration))
        dur_entry.pack()

        tk.Label(dialog, text="Description").pack(pady=5)
        desc_text = tk.Text(dialog, height=4, width=30)
        desc_text.insert("1.0", film.description or "")
        desc_text.pack()

        def update_film():
            name = name_entry.get()
            genre = genre_entry.get()
            rating = rating_entry.get()
            dur = dur_entry.get()
            desc = desc_text.get("1.0", tk.END).strip()
            if name and genre and dur and rating:
                try:
                    from app.models.film import Film
                    updated_film = Film(film_id, name, genre, rating, desc, int(dur))
                    self.controller.update_film(updated_film)
                    self.refresh_films()
                    dialog.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Duration must be an integer (e.g. 120)")
            else:
                messagebox.showwarning("Warning", "All fields except Description are required")

        tk.Button(dialog, text="Update", command=update_film).pack(pady=20)

    def setup_user_tab(self):
        tk.Label(self.user_frame, text="User Management", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Table (Treeview)
        cols = ('ID', 'Username', 'Role', 'Created At')
        self.user_tree = ttk.Treeview(self.user_frame, columns=cols, show='headings')
        for col in cols:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=150)
        self.user_tree.pack(expand=True, fill='both', padx=10, pady=10)

        # Buttons
        btn_frame = tk.Frame(self.user_frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_users).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Add User", command=self.add_user_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete User", command=self.delete_user).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Edit User", command=self.edit_user_dialog).pack(side=tk.LEFT, padx=5)

        self.refresh_users()

    def refresh_users(self):
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        users = self.controller.get_all_users()
        for u in users:
            self.user_tree.insert('', tk.END, values=(u.user_id, u.username, u.role, u.created_at))

    def add_user_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New User")
        dialog.geometry("300x250")

        tk.Label(dialog, text="Username").pack(pady=5)
        username_entry = tk.Entry(dialog)
        username_entry.pack()

        tk.Label(dialog, text="Password").pack(pady=5)
        password_entry = tk.Entry(dialog, show="*")
        password_entry.pack()

        tk.Label(dialog, text="Role").pack(pady=5)
        role_var = tk.StringVar(value="Admin")
        role_opt = ttk.OptionMenu(dialog, role_var, "Admin", "Admin", "Manager", "Booking-Staff")
        role_opt.pack()

        def save_user():
            username = username_entry.get()
            password = password_entry.get()
            role = role_var.get()
            if username and password:
                from app.models.user import User
                new_user = User(None, username, password, role, None)
                self.controller.add_user(new_user)
                self.refresh_users()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "All fields are required")

        tk.Button(dialog, text="Save", command=save_user).pack(pady=20)

    def delete_user(self):
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a user first")
            return
        user_id = self.user_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", f"Delete user ID {user_id}?"):
            self.controller.delete_user(user_id)
            self.refresh_users()

    def edit_user_dialog(self):
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a user first")
            return
        
        user_id = self.user_tree.item(selected[0])['values'][0]
        current_username = self.user_tree.item(selected[0])['values'][1]
        current_role = self.user_tree.item(selected[0])['values'][2]

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit User")
        dialog.geometry("300x250")

        tk.Label(dialog, text="Username").pack(pady=5)
        username_entry = tk.Entry(dialog)
        username_entry.insert(0, current_username)
        username_entry.pack()

        tk.Label(dialog, text="Password (leave blank to keep current)").pack(pady=5)
        password_entry = tk.Entry(dialog, show="*")
        password_entry.pack()

        tk.Label(dialog, text="Role").pack(pady=5)
        role_var = tk.StringVar(value=current_role)
        role_opt = ttk.OptionMenu(dialog, role_var, current_role, "Admin", "Manager", "Booking-Staff")
        role_opt.pack()

        def update_user():
            username = username_entry.get()
            password = password_entry.get()
            role = role_var.get()
            if username:
                from app.models.user import User
                users = self.controller.get_all_users()
                target_user = next((u for u in users if u.user_id == user_id), None)
                if not target_user:
                    messagebox.showerror("Error", "User not found")
                    return
                
                # If password is provided, we update it, else keep old
                new_pass = password if password else target_user.password
                
                updated_user = User(user_id, username, new_pass, role, target_user.created_at)
                # update_user method in user repo updates the password_hash directly.
                # If it expects plain text, we would need to hash it. Assuming the repository handles it or we pass it as is.
                # Looking at original add_user, password is passed as is.
                self.controller.update_user(updated_user)
                self.refresh_users()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "Username is required")

        tk.Button(dialog, text="Update", command=update_user).pack(pady=20)


    # --- Stubs for other tabs ---
    def setup_cinema_tab(self):
        tk.Label(self.cinema_frame, text="Cinema Management", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Table (Treeview)
        cols = ('ID', 'Name', 'City')
        self.cinema_tree = ttk.Treeview(self.cinema_frame, columns=cols, show='headings')
        for col in cols:
            self.cinema_tree.heading(col, text=col)
            self.cinema_tree.column(col, width=150)
        self.cinema_tree.pack(expand=True, fill='both', padx=10, pady=10)

        # Buttons
        btn_frame = tk.Frame(self.cinema_frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_cinemas).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Add Cinema", command=self.add_cinema_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Cinema", command=self.delete_cinema).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Edit Cinema", command=self.edit_cinema_dialog).pack(side=tk.LEFT, padx=5)

        self.refresh_cinemas()

    def refresh_cinemas(self):
        for item in self.cinema_tree.get_children():
            self.cinema_tree.delete(item)
        cinemas = self.controller.get_all_cinemas()
        for c in cinemas:
            self.cinema_tree.insert('', tk.END, values=(c.id, c.name, c.get_city_name()))

    def add_cinema_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Cinema")
        dialog.geometry("300x200")

        tk.Label(dialog, text="Name").pack(pady=5)
        name_entry = tk.Entry(dialog)
        name_entry.pack()

        tk.Label(dialog, text="City").pack(pady=5)
        cities = self.controller.get_all_cities()
        city_names = [c.name for c in cities]
        city_map = {c.name: c.id for c in cities}
        
        city_combo = ttk.Combobox(dialog, values=city_names, state="readonly")
        city_combo.pack()
        if city_names:
            city_combo.current(0)

        def save_cinema():
            name = name_entry.get()
            city_name = city_combo.get()
            if name and city_name:
                city_id = city_map[city_name]
                from app.models.cinema import Cinema
                new_cinema = Cinema(None, name, city_id)
                self.controller.add_cinema(new_cinema)
                self.refresh_cinemas()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "All fields are required")

        tk.Button(dialog, text="Save", command=save_cinema).pack(pady=20)

    def delete_cinema(self):
        selected = self.cinema_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a cinema first")
            return
        cinema_id = self.cinema_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", f"Delete cinema ID {cinema_id}?"):
            self.controller.delete_cinema(cinema_id)
            self.refresh_cinemas()

    def edit_cinema_dialog(self):
        selected = self.cinema_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a cinema first")
            return
        
        cinema_id = self.cinema_tree.item(selected[0])['values'][0]
        current_name = self.cinema_tree.item(selected[0])['values'][1]
        current_city = self.cinema_tree.item(selected[0])['values'][2]

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Cinema")
        dialog.geometry("300x200")

        tk.Label(dialog, text="Name").pack(pady=5)
        name_entry = tk.Entry(dialog)
        name_entry.insert(0, current_name)
        name_entry.pack()

        tk.Label(dialog, text="City").pack(pady=5)
        cities = self.controller.get_all_cities()
        city_names = [c.name for c in cities]
        city_map = {c.name: c.id for c in cities}
        
        city_combo = ttk.Combobox(dialog, values=city_names, state="readonly")
        city_combo.pack()
        if current_city in city_names:
            city_combo.set(current_city)
        elif city_names:
            city_combo.current(0)

        def update_cinema():
            name = name_entry.get()
            city_name = city_combo.get()
            if name and city_name:
                city_id_val = city_map[city_name]
                from app.models.cinema import Cinema
                updated_cinema = Cinema(cinema_id, name, city_id_val)
                self.controller.update_cinema(updated_cinema)
                self.refresh_cinemas()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "All fields are required")

        tk.Button(dialog, text="Update", command=update_cinema).pack(pady=20)


    def setup_screen_tab(self):
        tk.Label(self.screen_frame, text="Screen Management", font=("Arial", 16, "bold")).pack(pady=10)
        
        cols = ('ID', 'Cinema', 'Number', 'Capacity')
        self.screen_tree = ttk.Treeview(self.screen_frame, columns=cols, show='headings')
        for col in cols:
            self.screen_tree.heading(col, text=col)
            self.screen_tree.column(col, width=150)
        self.screen_tree.pack(expand=True, fill='both', padx=10, pady=10)

        btn_frame = tk.Frame(self.screen_frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_screens).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Add Screen", command=self.add_screen_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Screen", command=self.delete_screen).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Edit Screen", command=self.edit_screen_dialog).pack(side=tk.LEFT, padx=5)

        self.refresh_screens()

    def refresh_screens(self):
        for item in self.screen_tree.get_children():
            self.screen_tree.delete(item)
        screens = self.controller.get_all_screens()
        for s in screens:
            self.screen_tree.insert('', tk.END, values=(s.id, s.get_cinema_name(), s.screen_number, s.total_seats))

    def add_screen_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Screen")
        dialog.geometry("300x250")

        tk.Label(dialog, text="Cinema").pack(pady=5)
        cinemas = self.controller.get_all_cinemas()
        cinema_names = [c.name for c in cinemas]
        cinema_map = {c.name: c.id for c in cinemas}
        
        cinema_combo = ttk.Combobox(dialog, values=cinema_names, state="readonly")
        cinema_combo.pack()
        if cinema_names:
            cinema_combo.current(0)

        tk.Label(dialog, text="Screen Number").pack(pady=5)
        num_entry = tk.Entry(dialog)
        num_entry.pack()

        tk.Label(dialog, text="Total Seats").pack(pady=5)
        seats_entry = tk.Entry(dialog)
        seats_entry.pack()

        def save_screen():
            cinema_name = cinema_combo.get()
            num = num_entry.get()
            seats = seats_entry.get()
            if cinema_name and num and seats:
                cinema_id = cinema_map[cinema_name]
                from app.models.screen import Screen
                new_screen = Screen(None, cinema_id, int(num), int(seats))
                self.controller.add_screen(new_screen)
                self.refresh_screens()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "All fields are required")

        tk.Button(dialog, text="Save", command=save_screen).pack(pady=20)

    def delete_screen(self):
        selected = self.screen_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a screen first")
            return
        screen_id = self.screen_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", f"Delete screen ID {screen_id}?"):
            self.controller.delete_screen(screen_id)
            self.refresh_screens()

    def edit_screen_dialog(self):
        selected = self.screen_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a screen first")
            return
        
        screen_id = self.screen_tree.item(selected[0])['values'][0]
        current_cinema = self.screen_tree.item(selected[0])['values'][1]
        current_num = self.screen_tree.item(selected[0])['values'][2]
        current_seats = self.screen_tree.item(selected[0])['values'][3]

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Screen")
        dialog.geometry("300x250")

        tk.Label(dialog, text="Cinema").pack(pady=5)
        cinemas = self.controller.get_all_cinemas()
        cinema_names = [c.name for c in cinemas]
        cinema_map = {c.name: c.id for c in cinemas}
        
        cinema_combo = ttk.Combobox(dialog, values=cinema_names, state="readonly")
        cinema_combo.pack()
        if current_cinema in cinema_names:
            cinema_combo.set(current_cinema)
        elif cinema_names:
            cinema_combo.current(0)

        tk.Label(dialog, text="Screen Number").pack(pady=5)
        num_entry = tk.Entry(dialog)
        num_entry.insert(0, str(current_num))
        num_entry.pack()

        tk.Label(dialog, text="Total Seats").pack(pady=5)
        seats_entry = tk.Entry(dialog)
        seats_entry.insert(0, str(current_seats))
        seats_entry.pack()

        def update_screen():
            cinema_name = cinema_combo.get()
            num = num_entry.get()
            seats = seats_entry.get()
            if cinema_name and num and seats:
                cinema_id_val = cinema_map[cinema_name]
                from app.models.screen import Screen
                updated_screen = Screen(screen_id, cinema_id_val, int(num), int(seats))
                self.controller.update_screen(updated_screen)
                self.refresh_screens()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "All fields are required")

        tk.Button(dialog, text="Update", command=update_screen).pack(pady=20)


    def setup_seat_tab(self):
        tk.Label(self.seat_frame, text="Seat Management", font=("Arial", 16, "bold")).pack(pady=10)
        
        cols = ('ID', 'Screen', 'Number', 'Type')
        self.seat_tree = ttk.Treeview(self.seat_frame, columns=cols, show='headings')
        for col in cols:
            self.seat_tree.heading(col, text=col)
            self.seat_tree.column(col, width=200)
        self.seat_tree.pack(expand=True, fill='both', padx=10, pady=10)

        btn_frame = tk.Frame(self.seat_frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_seats).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Add Seat", command=self.add_seat_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Seat", command=self.delete_seat).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Edit Seat", command=self.edit_seat_dialog).pack(side=tk.LEFT, padx=5)

        self.refresh_seats()

    def refresh_seats(self):
        for item in self.seat_tree.get_children():
            self.seat_tree.delete(item)
        seats = self.controller.get_all_seats()
        for s in seats:
            self.seat_tree.insert('', tk.END, values=(s.id, s.get_screen_info(), s.seat_number, s.seat_type))

    def add_seat_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Seat")
        dialog.geometry("300x250")

        tk.Label(dialog, text="Screen").pack(pady=5)
        screens = self.controller.get_all_screens()
        # We'll show "Cinema Name - Screen Number" for clarity
        # Requirement: get_all_cinemas to lookup names
        cinemas = self.controller.get_all_cinemas()
        c_map = {c.id: c.name for c in cinemas}
        
        screen_labels = [f"{c_map.get(s.cinema_id, 'Unknown')} - Screen {s.screen_number}" for s in screens]
        screen_map = {f"{c_map.get(s.cinema_id, 'Unknown')} - Screen {s.screen_number}": s.id for s in screens}

        screen_combo = ttk.Combobox(dialog, values=screen_labels, state="readonly")
        screen_combo.pack()
        if screen_labels:
            screen_combo.current(0)

        tk.Label(dialog, text="Seat Number (e.g. A1)").pack(pady=5)
        num_entry = tk.Entry(dialog)
        num_entry.pack()

        tk.Label(dialog, text="Type").pack(pady=5)
        type_var = tk.StringVar(value="Lower")
        type_opt = ttk.OptionMenu(dialog, type_var, "Lower", "Lower", "Upper", "VIP")
        type_opt.pack()

        def save_seat():
            screen_label = screen_combo.get()
            num = num_entry.get()
            stype = type_var.get()
            if screen_label and num:
                screen_id = screen_map[screen_label]
                from app.models.seat import Seat
                new_seat = Seat(None, screen_id, num, stype)
                self.controller.add_seat(new_seat)
                self.refresh_seats()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "All fields are required")

        tk.Button(dialog, text="Save", command=save_seat).pack(pady=20)

    def delete_seat(self):
        selected = self.seat_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a seat first")
            return
        seat_id = self.seat_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", f"Delete seat ID {seat_id}?"):
            self.controller.delete_seat(seat_id)
            self.refresh_seats()

    def edit_seat_dialog(self):
        selected = self.seat_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a seat first")
            return
        
        seat_id = self.seat_tree.item(selected[0])['values'][0]
        current_screen_info = self.seat_tree.item(selected[0])['values'][1]
        current_num = self.seat_tree.item(selected[0])['values'][2]
        current_type = self.seat_tree.item(selected[0])['values'][3]

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Seat")
        dialog.geometry("300x250")

        tk.Label(dialog, text="Screen").pack(pady=5)
        screens = self.controller.get_all_screens()
        cinemas = self.controller.get_all_cinemas()
        c_map = {c.id: c.name for c in cinemas}
        
        screen_labels = [f"{c_map.get(s.cinema_id, 'Unknown')} - Screen {s.screen_number}" for s in screens]
        screen_map = {f"{c_map.get(s.cinema_id, 'Unknown')} - Screen {s.screen_number}": s.id for s in screens}

        screen_combo = ttk.Combobox(dialog, values=screen_labels, state="readonly")
        screen_combo.pack()
        if current_screen_info in screen_labels:
            screen_combo.set(current_screen_info)
        elif screen_labels:
            screen_combo.current(0)

        tk.Label(dialog, text="Seat Number (e.g. A1)").pack(pady=5)
        num_entry = tk.Entry(dialog)
        num_entry.insert(0, current_num)
        num_entry.pack()

        tk.Label(dialog, text="Type").pack(pady=5)
        type_var = tk.StringVar(value=current_type)
        type_opt = ttk.OptionMenu(dialog, type_var, current_type, "Lower", "Upper", "VIP")
        type_opt.pack()

        def update_seat():
            screen_label = screen_combo.get()
            num = num_entry.get()
            stype = type_var.get()
            if screen_label and num:
                screen_id_val = screen_map[screen_label]
                from app.models.seat import Seat
                updated_seat = Seat(seat_id, screen_id_val, num, stype)
                self.controller.update_seat(updated_seat)
                self.refresh_seats()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "All fields are required")

        tk.Button(dialog, text="Update", command=update_seat).pack(pady=20)


    def setup_booking_tab(self):
        tk.Label(self.booking_frame, text="Booking Management", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Table (Treeview)
        cols = ('ID', 'Ref', 'User ID', 'Show ID', 'Price', 'Status', 'Date')
        self.booking_tree = ttk.Treeview(self.booking_frame, columns=cols, show='headings')
        for col in cols:
            self.booking_tree.heading(col, text=col)
            self.booking_tree.column(col, width=120)
        self.booking_tree.pack(expand=True, fill='both', padx=10, pady=10)

        # Buttons
        btn_frame = tk.Frame(self.booking_frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_bookings).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel Booking", command=self.cancel_booking).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Edit Booking", command=self.edit_booking_dialog).pack(side=tk.LEFT, padx=5)

        self.refresh_bookings()

    def refresh_bookings(self):
        for item in self.booking_tree.get_children():
            self.booking_tree.delete(item)
        bookings = self.controller.get_all_bookings()
        for b in bookings:
            self.booking_tree.insert('', tk.END, values=(b.id, b.booking_ref, b.user_id, b.show_id, b.total_price, b.status, b.booking_date))

    def cancel_booking(self):
        selected = self.booking_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a booking first")
            return
        booking_id = self.booking_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", f"Cancel booking ID {booking_id}?"):
            # Update status to CANCELLED instead of hard delete if preferred
            # For simplicity in this CRUD, we'll just demonstrate delete or status update
            # The current repository has delete_booking
            self.controller.delete_booking(booking_id)
            self.refresh_bookings()

    def edit_booking_dialog(self):
        selected = self.booking_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a booking first")
            return
        
        booking_id = self.booking_tree.item(selected[0])['values'][0]
        ref = self.booking_tree.item(selected[0])['values'][1]
        user_id = self.booking_tree.item(selected[0])['values'][2]
        show_id = self.booking_tree.item(selected[0])['values'][3]
        price = self.booking_tree.item(selected[0])['values'][4]
        current_status = self.booking_tree.item(selected[0])['values'][5]
        b_date = self.booking_tree.item(selected[0])['values'][6]

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Booking")
        dialog.geometry("300x200")

        tk.Label(dialog, text=f"Booking Ref: {ref}").pack(pady=5)
        
        tk.Label(dialog, text="Status").pack(pady=5)
        status_var = tk.StringVar(value=current_status)
        status_opt = ttk.OptionMenu(dialog, status_var, current_status, "Confirmed", "Cancelled", "Pending")
        status_opt.pack()

        def update_booking():
            status = status_var.get()
            if status:
                from app.models.booking import Booking
                updated_booking = Booking(booking_id, user_id, show_id, float(price), status, ref, b_date)
                self.controller.update_booking(updated_booking)
                self.refresh_bookings()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "Status is required")

        tk.Button(dialog, text="Update", command=update_booking).pack(pady=20)


if __name__ == "__main__":
    # Test
    from app.models.user import User
    AdminPanel(User(1, 'admin_test', 'pass', 'Admin', 'none'))
