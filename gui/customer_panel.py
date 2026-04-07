import tkinter as tk
from tkinter import ttk, messagebox

class CustomerPanel:
    def __init__(self, user):
        self.user = user
        self.root = tk.Tk()
        self.root.title(f"Horizon Cinema - Customer Portal: {user.username}")
        self.root.geometry("1000x700")

        # Basic Controller Integration (Shared with Admin for simplicity in this project)
        from app.controllers.admin_controller import AdminController
        self.controller = AdminController()

        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root)
        header_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(header_frame, text=f"Welcome, {self.user.username}", font=("Arial", 12)).pack(side=tk.LEFT)
        tk.Button(header_frame, text="Logout", command=self.logout).pack(side=tk.RIGHT)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Tabs
        self.halls_frame = tk.Frame(self.notebook)
        self.my_bookings_frame = tk.Frame(self.notebook)

        self.notebook.add(self.halls_frame, text="Browse Theatre Halls")
        self.notebook.add(self.my_bookings_frame, text="My Bookings")

        self.setup_halls_tab()
        self.setup_my_bookings_tab()

    def logout(self):
        self.root.destroy()
        from gui.loginWindow import LoginWindow
        LoginWindow()

    def setup_halls_tab(self):
        # Top half: List of Cinemas
        tk.Label(self.halls_frame, text="Select a Cinema Hall", font=("Arial", 14, "bold")).pack(pady=10)
        
        cols = ('ID', 'Name', 'City')
        self.hall_tree = ttk.Treeview(self.halls_frame, columns=cols, show='headings', height=8)
        for col in cols:
            self.hall_tree.heading(col, text=col)
            self.hall_tree.column(col, width=200)
        self.hall_tree.pack(fill='x', padx=10, pady=5)
        self.hall_tree.bind('<<TreeviewSelect>>', self.on_hall_select)

        # Bottom half: Movies in selected hall
        self.movie_section = tk.Frame(self.halls_frame)
        self.movie_section.pack(expand=True, fill='both', pady=10)
        
        tk.Label(self.movie_section, text="Available Movies", font=("Arial", 12, "bold")).pack()
        
        m_cols = ('ID', 'Movie', 'Genre', 'Rating', 'Duration')
        self.movie_tree = ttk.Treeview(self.movie_section, columns=m_cols, show='headings')
        for col in m_cols:
            self.movie_tree.heading(col, text=col)
            self.movie_tree.column(col, width=150)
        self.movie_tree.pack(expand=True, fill='both', padx=10, pady=5)
        self.movie_tree.bind('<<TreeviewSelect>>', self.on_movie_select)

        self.refresh_halls()

    def refresh_halls(self):
        for item in self.hall_tree.get_children():
            self.hall_tree.delete(item)
        cinemas = self.controller.get_all_cinemas()
        for c in cinemas:
            self.hall_tree.insert('', tk.END, values=(c.id, c.name, c.get_city_name()))

    def on_hall_select(self, event):
        selected = self.hall_tree.selection()
        if not selected: return
        cinema_id = self.hall_tree.item(selected[0])['values'][0]
        
        # Refresh movies for this cinema
        for item in self.movie_tree.get_children():
            self.movie_tree.delete(item)
            
        # We need a way to get distinct films for a cinema from shows
        shows = self.controller.get_all_shows(cinema_id=cinema_id)
        unique_films = {}
        for s in shows:
            if s.film_id not in unique_films:
                unique_films[s.film_id] = s
        
        # Actually need to fetch the full film model for rating/genre
        all_films = self.controller.get_all_films()
        film_dict = {f.id: f for f in all_films}
        
        for f_id in unique_films:
            f = film_dict.get(f_id)
            if f:
                self.movie_tree.insert('', tk.END, values=(f.id, f.name, f.genre, f.age_rating, f.time_duration))

    def on_movie_select(self, event):
        hall_sel = self.hall_tree.selection()
        movie_sel = self.movie_tree.selection()
        if not (hall_sel and movie_sel): return
        
        cinema_id = self.hall_tree.item(hall_sel[0])['values'][0]
        film_id = self.movie_tree.item(movie_sel[0])['values'][0]
        movie_name = self.movie_tree.item(movie_sel[0])['values'][1]

        # Open Show Selection Dialog
        self.open_booking_dialog(cinema_id, film_id, movie_name)

    def open_booking_dialog(self, cinema_id, film_id, movie_name):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Booking: {movie_name}")
        dialog.geometry("500x600")

        tk.Label(dialog, text=f"Available Shows for {movie_name}", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Show List
        s_cols = ('ID', 'Time', 'Screen', 'Price')
        show_tree = ttk.Treeview(dialog, columns=s_cols, show='headings', height=5)
        for col in s_cols:
            show_tree.heading(col, text=col)
            show_tree.column(col, width=100)
        show_tree.pack(fill='x', padx=10, pady=5)

        # Filter shows by cinema and film
        all_shows = self.controller.get_all_shows(cinema_id=cinema_id)
        target_shows = [s for s in all_shows if s.film_id == film_id]
        for s in target_shows:
            show_tree.insert('', tk.END, values=(s.id, s.show_time, s.screen_number, s.base_price))

        # Seat Section
        seat_frame = tk.LabelFrame(dialog, text="Select a Seat")
        seat_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        seat_cols = ('ID', 'Number', 'Type')
        seat_tree = ttk.Treeview(seat_frame, columns=seat_cols, show='headings')
        for col in seat_cols:
            seat_tree.heading(col, text=col)
            seat_tree.column(col, width=100)
        seat_tree.pack(expand=True, fill='both')

        def on_show_click(event):
            s_sel = show_tree.selection()
            if not s_sel: return
            item = show_tree.item(s_sel[0])
            show_id = item['values'][0]
            screen_num = item['values'][2]
            
            # Fetch seats for this screen
            # Need to find screen_id from screen_num and cinema_id
            screens = self.controller.get_all_screens()
            screen_id = None
            for sc in screens:
                if sc.cinema_id == cinema_id and sc.screen_number == screen_num:
                    screen_id = sc.id
                    break
            
            for i in seat_tree.get_children(): seat_tree.delete(i)
            if screen_id:
                seats = self.controller.seat_repo.get_all_seats() # Filtered by screen locally for now
                for st in seats:
                    if st.screen_id == screen_id:
                        seat_tree.insert('', tk.END, values=(st.id, st.seat_number, st.seat_type))

        show_tree.bind('<<TreeviewSelect>>', on_show_click)

        def confirm_booking():
            s_sel = show_tree.selection()
            st_sel = seat_tree.selection()
            if not (s_sel and st_sel):
                messagebox.showwarning("Warning", "Select both a Show and a Seat")
                return
            
            show_id = show_tree.item(s_sel[0])['values'][0]
            show_price = show_tree.item(s_sel[0])['values'][3]
            seat_id = seat_tree.item(st_sel[0])['values'][0]
            seat_num = seat_tree.item(st_sel[0])['values'][1]

            if messagebox.askyesno("Confirm", f"Book Seat {seat_num} for ${show_price}?"):
                from app.models.booking import Booking
                import uuid
                from datetime import datetime
                ref = str(uuid.uuid4())[:8].upper()
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Params: id, booking_ref, user_id, show_id, promo_id, total_price, service_fee, status, booking_date, created_at
                new_booking = Booking(None, ref, self.user.user_id, show_id, None, show_price, 0.0, "CONFIRMED", now, now)
                self.controller.add_booking(new_booking)
                messagebox.showinfo("Success", f"Ticket Booked! Ref: {ref}")
                self.refresh_my_bookings()
                dialog.destroy()

        tk.Button(dialog, text="Confirm Booking", command=confirm_booking, bg="green", fg="white").pack(pady=10)

    def setup_my_bookings_tab(self):
        tk.Label(self.my_bookings_frame, text="My Movie Tickets", font=("Arial", 16, "bold")).pack(pady=10)
        
        cols = ('Ref', 'Movie', 'Time', 'Price', 'Status')
        self.my_tree = ttk.Treeview(self.my_bookings_frame, columns=cols, show='headings')
        for col in cols:
            self.my_tree.heading(col, text=col)
            self.my_tree.column(col, width=150)
        self.my_tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        tk.Button(self.my_bookings_frame, text="Refresh", command=self.refresh_my_bookings).pack(pady=10)
        self.refresh_my_bookings()

    def refresh_my_bookings(self):
        for item in self.my_tree.get_children():
            self.my_tree.delete(item)
            
        # Ideally BookingRepository should have get_by_user
        all_bookings = self.controller.get_all_bookings()
        my_bookings = [b for b in all_bookings if b.user_id == self.user.user_id]
        
        # Need movie names and times too
        all_shows = self.controller.get_all_shows()
        show_dict = {s.id: s for s in all_shows}

        for b in my_bookings:
            s = show_dict.get(b.show_id)
            movie = s.film_name if s else "Unknown"
            time = s.show_time if s else "Unknown"
            self.my_tree.insert('', tk.END, values=(b.booking_ref, movie, time, b.total_price, b.status))
