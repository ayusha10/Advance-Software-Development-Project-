import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.admin_controller import AdminController
from gui.theme import Theme

class ManagerPanel:
    def __init__(self, user):
        self.user = user
        self.controller = AdminController()
        
        self.root = tk.Tk()
        self.root.title(f"Manager Dashboard - {self.user.username}")
        self.root.geometry("1100x800")
        
        # Apply Modern Theme
        Theme.apply(self.root)

        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        # Header with Logout
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill='x', padx=20, pady=20)
        
        ttk.Label(header_frame, text=f"HORIZON CINEMA MANAGER", style="Header.TLabel").pack(side=tk.LEFT)
        
        user_info = ttk.Frame(header_frame)
        user_info.pack(side=tk.RIGHT)
        ttk.Label(user_info, text=f"Logged in as: {self.user.username} (Manager)", font=Theme.FONT_BOLD).pack(side=tk.LEFT, padx=10)
        ttk.Button(user_info, text="Logout", command=self.logout, style="Danger.TButton").pack(side=tk.LEFT)

        # Notebook for TABS
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        self.create_tabs()

    def logout(self):
        self.root.destroy()
        from gui.loginWindow import LoginWindow
        LoginWindow()

    def create_tabs(self):
        # Cinemas Tab
        self.cinema_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.cinema_frame, text="Cinemas Management")
        self.setup_cinema_tab()

        # Screens Tab
        self.screen_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.screen_frame, text="Screens Management")
        self.setup_screen_tab()

        # Seats Tab
        self.seat_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.seat_frame, text="Seats Management")
        self.setup_seat_tab()

        # Bookings Tab
        self.booking_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.booking_frame, text="Booking Management")
        self.setup_booking_tab()

        # Films Tab
        self.film_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.film_frame, text="Film Management")
        self.setup_film_tab()

        # Shows Tab
        self.show_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.show_frame, text="Show Management")
        self.setup_show_tab()

    def setup_show_tab(self):
        ttk.Label(self.show_frame, text="Show Management", font=("Arial", 16, "bold")).pack(fill='x', pady=10)
        
        cols = ('ID', 'Film', 'Screen', 'Time', 'Price')
        self.show_tree = ttk.Treeview(self.show_frame, columns=cols, show='headings')
        for col in cols:
            self.show_tree.heading(col, text=col, anchor='center')
            self.show_tree.column(col, width=150, anchor='center')
        self.show_tree.pack(expand=True, fill='both', padx=10, pady=10)

        btn_frame = ttk.Frame(self.show_frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_shows).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Show", command=self.add_show_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Show", command=self.delete_show).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit Show", command=self.edit_show_dialog).pack(side=tk.LEFT, padx=5)

        self.refresh_shows()

    def refresh_shows(self):
        for item in self.show_tree.get_children():
            self.show_tree.delete(item)
        
        all_shows = self.controller.get_all_shows()
        city_cinemas = [c.id for c in self.controller.get_all_cinemas() if c.city_id == self.user.assigned_city_id]
        all_screens = self.controller.get_all_screens()
        valid_screens = [s.id for s in all_screens if s.cinema_id in city_cinemas]

        for s in all_shows:
            if s.screen_id in valid_screens:
                self.show_tree.insert('', tk.END, values=(
                    s.id, s.film_name, s.screen_number, s.show_time, s.base_price
                ))

    def add_show_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Schedule New Show")
        dialog.geometry("500x700")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Select Film").pack(fill='x', pady=5)
        films = self.controller.get_all_films()
        film_map = {f.name: f.id for f in films}
        film_combo = ttk.Combobox(container, values=list(film_map.keys()), state="readonly")
        film_combo.pack(fill='x')

        ttk.Label(container, text="Select Screen").pack(fill='x', pady=5)
        # Filtered by manager's cinema
        all_screens = self.controller.get_all_screens()
        city_cinemas = [c.id for c in self.controller.get_all_cinemas() if c.city_id == self.user.assigned_city_id]
        screens = [s for s in all_screens if s.cinema_id in city_cinemas]
        screen_map = {f"Screen {s.screen_number}": s.id for s in screens}
        screen_combo = ttk.Combobox(container, values=list(screen_map.keys()), state="readonly")
        screen_combo.pack(fill='x')

        ttk.Label(container, text="Show Date (YYYY-MM-DD)").pack(fill='x', pady=5)
        date_entry = ttk.Entry(container, width=30)
        date_entry.insert(0, "2026-04-10")
        date_entry.pack(fill='x')

        ttk.Label(container, text="Show Time (HH:MM:SS)").pack(fill='x', pady=5)
        time_entry = ttk.Entry(container, width=30)
        time_entry.insert(0, "18:00:00")
        time_entry.pack(fill='x')

        ttk.Label(container, text="Base Price").pack(fill='x', pady=5)
        price_entry = ttk.Entry(container, width=30)
        price_entry.insert(0, "10.00")
        price_entry.pack(fill='x')

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

        ttk.Button(container, text="Save Show", command=save_show).pack(fill='x', pady=20)

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
        dialog.geometry("500x700")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Select Film").pack(fill='x', pady=5)
        films = self.controller.get_all_films()
        film_map = {f.name: f.id for f in films}
        film_combo = ttk.Combobox(container, values=list(film_map.keys()), state="readonly")
        film_combo.pack(fill='x')
        if show.film_name in film_map:
            film_combo.set(show.film_name)

        ttk.Label(container, text="Select Screen").pack(fill='x', pady=5)
        all_screens = self.controller.get_all_screens()
        city_cinemas = [c.id for c in self.controller.get_all_cinemas() if c.city_id == self.user.assigned_city_id]
        screens = [s for s in all_screens if s.cinema_id in city_cinemas]
        screen_map = {f"Screen {s.screen_number}": s.id for s in screens}
        screen_combo = ttk.Combobox(container, values=list(screen_map.keys()), state="readonly")
        screen_combo.pack(fill='x')
        screen_label = f"Screen {show.screen_number}"
        if screen_label in screen_map:
            screen_combo.set(screen_label)

        ttk.Label(container, text="Show Date (YYYY-MM-DD)").pack(fill='x', pady=5)
        date_entry = ttk.Entry(container, width=30)
        date_entry.insert(0, show.show_date)
        date_entry.pack(fill='x')

        ttk.Label(container, text="Show Time (HH:MM:SS)").pack(fill='x', pady=5)
        time_entry = ttk.Entry(container, width=30)
        time_entry.insert(0, show.show_time)
        time_entry.pack(fill='x')

        ttk.Label(container, text="Base Price").pack(fill='x', pady=5)
        price_entry = ttk.Entry(container, width=30)
        price_entry.insert(0, str(show.base_price))
        price_entry.pack(fill='x')

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

        ttk.Button(container, text="Update Show", command=update_show).pack(fill='x', pady=20)


    def setup_film_tab(self):
        ttk.Label(self.film_frame, text="Film Management", font=("Arial", 16, "bold")).pack(fill='x', pady=10)
        
        cols = ('ID', 'Name', 'Genre', 'Rating', 'Duration')
        self.film_tree = ttk.Treeview(self.film_frame, columns=cols, show='headings')
        for col in cols:
            self.film_tree.heading(col, text=col, anchor='center')
            self.film_tree.column(col, width=120, anchor='center')
        self.film_tree.pack(expand=True, fill='both', padx=10, pady=10)

        btn_frame = ttk.Frame(self.film_frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_films).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Film", command=self.add_film_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Film", command=self.delete_film).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit Film", command=self.edit_film_dialog).pack(side=tk.LEFT, padx=5)

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
        dialog.geometry("500x700")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Name").pack(fill='x', pady=5)
        name_entry = ttk.Entry(container, width=30)
        name_entry.pack(fill='x')

        ttk.Label(container, text="Genre").pack(fill='x', pady=5)
        genre_entry = ttk.Entry(container, width=30)
        genre_entry.pack(fill='x')

        ttk.Label(container, text="Age Rating").pack(fill='x', pady=5)
        rating_entry = ttk.Entry(container, width=30)
        rating_entry.pack(fill='x')

        ttk.Label(container, text="Duration (mins)").pack(fill='x', pady=5)
        dur_entry = ttk.Entry(container, width=30)
        dur_entry.pack(fill='x')

        ttk.Label(container, text="Description").pack(fill='x', pady=5)
        desc_text = tk.Text(container, height=4, width=30)
        desc_text.pack(fill='x')

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

        ttk.Button(container, text="Save", command=save_film).pack(fill='x', pady=20)

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
        films = self.controller.get_all_films()
        film = next((f for f in films if f.id == film_id), None)
        if not film:
            messagebox.showerror("Error", "Film not found")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Film")
        dialog.geometry("500x700")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Name").pack(fill='x', pady=5)
        name_entry = ttk.Entry(container, width=30)
        name_entry.insert(0, film.name)
        name_entry.pack(fill='x')

        ttk.Label(container, text="Genre").pack(fill='x', pady=5)
        genre_entry = ttk.Entry(container, width=30)
        genre_entry.insert(0, film.genre)
        genre_entry.pack(fill='x')

        ttk.Label(container, text="Age Rating").pack(fill='x', pady=5)
        rating_entry = ttk.Entry(container, width=30)
        rating_entry.insert(0, film.age_rating)
        rating_entry.pack(fill='x')

        ttk.Label(container, text="Duration (mins)").pack(fill='x', pady=5)
        dur_entry = ttk.Entry(container, width=30)
        dur_entry.insert(0, str(film.time_duration))
        dur_entry.pack(fill='x')

        ttk.Label(container, text="Description").pack(fill='x', pady=5)
        desc_text = tk.Text(container, height=4, width=30)
        desc_text.insert("1.0", film.description or "")
        desc_text.pack(fill='x')

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

        ttk.Button(container, text="Update", command=update_film).pack(fill='x', pady=20)



    # --- CINEMA TAB ---
    def setup_cinema_tab(self):
        ttk.Label(self.cinema_frame, text="Cinema Management", font=("Arial", 16, "bold")).pack(fill='x', pady=10)
        
        cols = ('ID', 'Name', 'City ID')
        self.cinema_tree = ttk.Treeview(self.cinema_frame, columns=cols, show='headings')
        for col in cols:
            self.cinema_tree.heading(col, text=col, anchor='center')
            self.cinema_tree.column(col, width=200, anchor='center')
        self.cinema_tree.pack(expand=True, fill='both', padx=10, pady=10)

        btn_frame = ttk.Frame(self.cinema_frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_cinemas).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Cinema", command=self.add_cinema_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit Cinema", command=self.edit_cinema_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Cinema", command=self.delete_cinema).pack(side=tk.LEFT, padx=5)

        self.refresh_cinemas()

    def refresh_cinemas(self):
        for item in self.cinema_tree.get_children():
            self.cinema_tree.delete(item)
        cinemas = self.controller.get_all_cinemas()
        for c in cinemas:
            if c.city_id == self.user.assigned_city_id:
                self.cinema_tree.insert('', tk.END, values=(c.id, c.name, c.city_id))

    def add_cinema_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Cinema")
        dialog.geometry("450x550")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Cinema Name").pack(fill='x', pady=5)
        name_entry = ttk.Entry(container)
        name_entry.pack(fill='x')

        def save_cinema():
            name = name_entry.get()
            if name:
                from app.models.cinema import Cinema
                new_cinema = Cinema(None, name, self.user.assigned_city_id)
                self.controller.add_cinema(new_cinema)
                self.refresh_cinemas()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "Cinema name is required")

        ttk.Button(container, text="Save", command=save_cinema).pack(fill='x', pady=10)

    def edit_cinema_dialog(self):
        selected = self.cinema_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a cinema first")
            return
        
        cinema_id = self.cinema_tree.item(selected[0])['values'][0]
        current_name = self.cinema_tree.item(selected[0])['values'][1]

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Cinema")
        dialog.geometry("450x550")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Cinema Name").pack(fill='x', pady=5)
        name_entry = ttk.Entry(container)
        name_entry.insert(0, current_name)
        name_entry.pack(fill='x')

        def update_cinema():
            name = name_entry.get()
            if name:
                from app.models.cinema import Cinema
                updated_cinema = Cinema(cinema_id, name, self.user.assigned_city_id)
                self.controller.update_cinema(updated_cinema)
                self.refresh_cinemas()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "Cinema name is required")

        ttk.Button(container, text="Update", command=update_cinema).pack(fill='x', pady=10)

    def delete_cinema(self):
        selected = self.cinema_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a cinema first")
            return
        cinema_id = self.cinema_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", f"Delete cinema ID {cinema_id}?"):
            self.controller.delete_cinema(cinema_id)
            self.refresh_cinemas()

    # --- SCREEN TAB ---
    def setup_screen_tab(self):
        ttk.Label(self.screen_frame, text="Screens Management", font=("Arial", 16, "bold")).pack(fill='x', pady=10)
        
        cols = ('ID', 'Cinema', 'Number', 'Capacity')
        self.screen_tree = ttk.Treeview(self.screen_frame, columns=cols, show='headings')
        for col in cols:
            self.screen_tree.heading(col, text=col, anchor='center')
            self.screen_tree.column(col, width=150, anchor='center')
        self.screen_tree.pack(expand=True, fill='both', padx=10, pady=10)

        btn_frame = ttk.Frame(self.screen_frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_screens).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Screen", command=self.add_screen_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Screen", command=self.delete_screen).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit Screen", command=self.edit_screen_dialog).pack(side=tk.LEFT, padx=5)
        
        self.refresh_screens()

    def refresh_screens(self):
        for item in self.screen_tree.get_children():
            self.screen_tree.delete(item)
        
        all_screens = self.controller.get_all_screens()
        city_cinemas = [c.id for c in self.controller.get_all_cinemas() if c.city_id == self.user.assigned_city_id]
        
        for s in all_screens:
            if s.cinema_id in city_cinemas:
                self.screen_tree.insert('', tk.END, values=(s.id, s.get_cinema_name(), s.screen_number, s.total_seats))

    def add_screen_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Screen")
        dialog.geometry("450x550")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Select Cinema").pack(fill='x', pady=5)
        cinemas = [c for c in self.controller.get_all_cinemas() if c.city_id == self.user.assigned_city_id]
        cinema_map = {c.name: c.id for c in cinemas}
        cinema_combo = ttk.Combobox(container, values=list(cinema_map.keys()), state="readonly")
        cinema_combo.pack(fill='x')

        ttk.Label(container, text="Screen Number").pack(fill='x', pady=5)
        num_entry = ttk.Entry(container)
        num_entry.pack(fill='x')

        ttk.Label(container, text="Total Seats").pack(fill='x', pady=5)
        seats_entry = ttk.Entry(container)
        seats_entry.pack(fill='x')

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

        ttk.Button(container, text="Save", command=save_screen).pack(fill='x', pady=20)

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
        current_num = self.screen_tree.item(selected[0])['values'][2]
        current_seats = self.screen_tree.item(selected[0])['values'][3]

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Screen")
        dialog.geometry("450x550")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Select Cinema").pack(fill='x', pady=5)
        cinemas = [c for c in self.controller.get_all_cinemas() if c.city_id == self.user.assigned_city_id]
        cinema_map = {c.name: c.id for c in cinemas}
        cinema_combo = ttk.Combobox(container, values=list(cinema_map.keys()), state="readonly")
        cinema_combo.pack(fill='x')

        ttk.Label(container, text="Screen Number").pack(fill='x', pady=5)
        num_entry = ttk.Entry(container)
        num_entry.insert(0, str(current_num))
        num_entry.pack(fill='x')

        ttk.Label(container, text="Total Seats").pack(fill='x', pady=5)
        seats_entry = ttk.Entry(container)
        seats_entry.insert(0, str(current_seats))
        seats_entry.pack(fill='x')

        def update_screen():
            cinema_name = cinema_combo.get()
            num = num_entry.get()
            seats = seats_entry.get()
            if cinema_name and num and seats:
                cinema_id = cinema_map[cinema_name]
                from app.models.screen import Screen
                updated_screen = Screen(screen_id, cinema_id, int(num), int(seats))
                self.controller.update_screen(updated_screen)
                self.refresh_screens()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "All fields are required")

        ttk.Button(container, text="Update", command=update_screen).pack(fill='x', pady=20)


    # --- SEAT TAB ---
    def setup_seat_tab(self):
        ttk.Label(self.seat_frame, text="Seat Management", font=("Arial", 16, "bold")).pack(fill='x', pady=10)
        
        cols = ('ID', 'Screen', 'Number', 'Type')
        self.seat_tree = ttk.Treeview(self.seat_frame, columns=cols, show='headings')
        for col in cols:
            self.seat_tree.heading(col, text=col, anchor='center')
            self.seat_tree.column(col, width=200, anchor='center')
        self.seat_tree.pack(expand=True, fill='both', padx=10, pady=10)

        btn_frame = ttk.Frame(self.seat_frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_seats).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Seat", command=self.add_seat_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Seat", command=self.delete_seat).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit Seat", command=self.edit_seat_dialog).pack(side=tk.LEFT, padx=5)
        self.refresh_seats()

    def refresh_seats(self):
        for item in self.seat_tree.get_children():
            self.seat_tree.delete(item)
        
        seats = self.controller.get_all_seats()
        all_screens = self.controller.get_all_screens()
        city_cinemas = [c.id for c in self.controller.get_all_cinemas() if c.city_id == self.user.assigned_city_id]
        valid_screens = [s.id for s in all_screens if s.cinema_id in city_cinemas]
        
        for s in seats:
            if s.screen_id in valid_screens:
                self.seat_tree.insert('', tk.END, values=(s.id, s.get_screen_info(), s.seat_number, s.seat_type))

    def add_seat_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Seat")
        dialog.geometry("450x550")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Select Screen").pack(fill='x', pady=5)
        all_screens = self.controller.get_all_screens()
        city_cinemas = [c.id for c in self.controller.get_all_cinemas() if c.city_id == self.user.assigned_city_id]
        screens = [s for s in all_screens if s.cinema_id in city_cinemas]
        screen_labels = [f"Screen {s.screen_number}" for s in screens]
        screen_map = {f"Screen {s.screen_number}": s.id for s in screens}

        screen_combo = ttk.Combobox(container, values=screen_labels, state="readonly")
        screen_combo.pack(fill='x')
        if screen_labels:
            screen_combo.current(0)

        ttk.Label(container, text="Seat Number (e.g. A1)").pack(fill='x', pady=5)
        num_entry = ttk.Entry(container)
        num_entry.pack(fill='x')

        ttk.Label(container, text="Type").pack(fill='x', pady=5)
        type_var = tk.StringVar(value="Lower")
        type_opt = ttk.OptionMenu(container, type_var, "Lower", "Lower", "Upper", "VIP")
        type_opt.pack(fill='x')

        def save_seat():
            screen_label = screen_combo.get()
            num = num_entry.get()
            stype = type_var.get()
            if screen_label and num:
                screen_id = screen_map[screen_label]
                from app.models.seat import Seat
                new_seat = Seat(id=None, screen_id=screen_id, seat_number=num, seat_type=stype)
                self.controller.add_seat(new_seat)
                self.refresh_seats()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "All fields are required")

        ttk.Button(container, text="Save", command=save_seat).pack(fill='x', pady=20)

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
        dialog.geometry("450x550")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Select Screen").pack(fill='x', pady=5)
        all_screens = self.controller.get_all_screens()
        city_cinemas = [c.id for c in self.controller.get_all_cinemas() if c.city_id == self.user.assigned_city_id]
        screens = [s for s in all_screens if s.cinema_id in city_cinemas]
        screen_labels = [f"Screen {s.screen_number}" for s in screens]
        screen_map = {f"Screen {s.screen_number}": s.id for s in screens}

        screen_combo = ttk.Combobox(container, values=screen_labels, state="readonly")
        screen_combo.pack(fill='x')
        # In manager panel, current_screen_info is likely "Cinema - Screen X". Let's extract just "Screen X"
        if "-" in current_screen_info:
            just_screen = current_screen_info.split("-")[-1].strip()
        else:
            just_screen = current_screen_info
            
        if just_screen in screen_labels:
            screen_combo.set(just_screen)
        elif screen_labels:
            screen_combo.current(0)

        ttk.Label(container, text="Seat Number (e.g. A1)").pack(fill='x', pady=5)
        num_entry = ttk.Entry(container)
        num_entry.insert(0, current_num)
        num_entry.pack(fill='x')

        ttk.Label(container, text="Type").pack(fill='x', pady=5)
        type_var = tk.StringVar(value=current_type)
        type_opt = ttk.OptionMenu(container, type_var, current_type, "Lower", "Upper", "VIP")
        type_opt.pack(fill='x')

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

        ttk.Button(container, text="Update", command=update_seat).pack(fill='x', pady=20)


    # --- BOOKING TAB ---
    def setup_booking_tab(self):
        ttk.Label(self.booking_frame, text="Booking Management", font=("Arial", 16, "bold")).pack(fill='x', pady=10)
        
        cols = ('ID', 'Reference', 'User ID', 'Show ID', 'Status', 'Date')
        self.booking_tree = ttk.Treeview(self.booking_frame, columns=cols, show='headings')
        for col in cols:
            self.booking_tree.heading(col, text=col, anchor='center')
            self.booking_tree.column(col, width=120, anchor='center')
        self.booking_tree.pack(expand=True, fill='both', padx=10, pady=10)

        btn_frame = ttk.Frame(self.booking_frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_bookings).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel Booking", command=self.cancel_booking).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit Booking", command=self.edit_booking_dialog).pack(side=tk.LEFT, padx=5)
        self.refresh_bookings()

    def refresh_bookings(self):
        for item in self.booking_tree.get_children():
            self.booking_tree.delete(item)
            
        bookings = self.controller.get_all_bookings()
        all_shows = self.controller.get_all_shows()
        all_screens = self.controller.get_all_screens()
        city_cinemas = [c.id for c in self.controller.get_all_cinemas() if c.city_id == self.user.assigned_city_id]
        valid_screens = [s.id for s in all_screens if s.cinema_id in city_cinemas]
        valid_shows = [s.id for s in all_shows if s.screen_id in valid_screens]
        
        for b in bookings:
            if b.show_id in valid_shows:
                self.booking_tree.insert('', tk.END, values=(
                    b.id, b.booking_ref, b.user_id, b.show_id, b.status, b.booking_date
                ))

    def cancel_booking(self):
        selected = self.booking_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a booking first")
            return
        booking_id = self.booking_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", f"Cancel/Delete booking ID {booking_id}?"):
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
        current_status = self.booking_tree.item(selected[0])['values'][4]
        b_date = self.booking_tree.item(selected[0])['values'][5]

        # Price isn't in tree, fetch from DB
        all_bookings = self.controller.get_all_bookings()
        booking = next((b for b in all_bookings if b.id == booking_id), None)
        price = booking.total_price if booking else 0.0

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Booking")
        dialog.geometry("450x550")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text=f"Booking Ref: {ref}").pack(fill='x', pady=5)
        
        ttk.Label(container, text="Status").pack(fill='x', pady=5)
        status_var = tk.StringVar(value=current_status)
        status_opt = ttk.OptionMenu(container, status_var, current_status, "Confirmed", "Cancelled", "Pending")
        status_opt.pack(fill='x')

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

        ttk.Button(container, text="Update", command=update_booking).pack(fill='x', pady=20)

