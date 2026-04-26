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
        self.movies_frame = tk.Frame(self.notebook)
        self.shows_frame = tk.Frame(self.notebook)
        self.booking_frame = tk.Frame(self.notebook)
        self.my_bookings_frame = tk.Frame(self.notebook)

        self.notebook.add(self.movies_frame, text="Browse Movies")
        self.notebook.add(self.shows_frame, text="Browse Shows")
        self.notebook.add(self.booking_frame, text="Book Tickets")
        self.notebook.add(self.my_bookings_frame, text="My Bookings")

        self.setup_movies_tab()
        self.setup_shows_tab()
        self.setup_booking_tab()
        self.setup_my_bookings_tab()

    def setup_movies_tab(self):
        tk.Label(self.movies_frame, text="Available Movies", font=("Arial", 16, "bold")).pack(pady=10)
        
        cols = ('ID', 'Name', 'Genre', 'Rating', 'Duration')
        self.movies_tree = ttk.Treeview(self.movies_frame, columns=cols, show='headings', height=15)
        for col in cols:
            self.movies_tree.heading(col, text=col)
            self.movies_tree.column(col, width=150)
        self.movies_tree.pack(expand=True, fill='both', padx=10, pady=5)
        
        tk.Button(self.movies_frame, text="Refresh Movies", command=self.refresh_movies).pack(pady=10)
        self.refresh_movies()

    def refresh_movies(self):
        for item in self.movies_tree.get_children():
            self.movies_tree.delete(item)
        
        films = self.controller.get_all_films()
        for film in films:
            self.movies_tree.insert('', tk.END, values=(film.id, film.name, film.genre, film.age_rating, f"{film.time_duration} min"))

    def setup_shows_tab(self):
        tk.Label(self.shows_frame, text="Available Shows", font=("Arial", 16, "bold")).pack(pady=10)
        
        cols = ('ID', 'Movie', 'Cinema', 'Screen', 'Date', 'Time', 'Price')
        self.shows_tree = ttk.Treeview(self.shows_frame, columns=cols, show='headings', height=15)
        for col in cols:
            self.shows_tree.heading(col, text=col)
            self.shows_tree.column(col, width=120)
        self.shows_tree.pack(expand=True, fill='both', padx=10, pady=5)
        
        tk.Button(self.shows_frame, text="Refresh Shows", command=self.refresh_shows).pack(pady=10)
        self.refresh_shows()

    def refresh_shows(self):
        for item in self.shows_tree.get_children():
            self.shows_tree.delete(item)
        
        shows = self.controller.get_all_shows()
        for show in shows:
            self.shows_tree.insert('', tk.END, values=(
                show.id, show.film_name, show.cinema_name, 
                show.screen_number, show.show_date, show.show_time, 
                f"${show.base_price}"
            ))

    def setup_booking_tab(self):
        tk.Label(self.booking_frame, text="Book Movie Tickets", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Show selection
        show_frame = tk.LabelFrame(self.booking_frame, text="Select Show")
        show_frame.pack(fill='x', padx=10, pady=5)
        
        cols = ('ID', 'Movie', 'Cinema', 'Screen', 'Date', 'Time', 'Price')
        self.booking_shows_tree = ttk.Treeview(show_frame, columns=cols, show='headings', height=8)
        for col in cols:
            self.booking_shows_tree.heading(col, text=col)
            self.booking_shows_tree.column(col, width=100)
        self.booking_shows_tree.pack(expand=True, fill='both', padx=5, pady=5)
        self.booking_shows_tree.bind('<<TreeviewSelect>>', self.on_show_select_for_booking)
        
        # Ticket and seat selection
        ticket_frame = tk.LabelFrame(self.booking_frame, text="Select Tickets & Seats")
        ticket_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Number of tickets
        tk.Label(ticket_frame, text="Number of Tickets:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.ticket_count = tk.IntVar(value=1)
        tk.Spinbox(ticket_frame, from_=1, to=10, textvariable=self.ticket_count).grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        # Available seats
        tk.Label(ticket_frame, text="Available Seats:").grid(row=1, column=0, padx=5, pady=5, sticky='nw')
        self.seats_listbox = tk.Listbox(ticket_frame, height=8, selectmode=tk.MULTIPLE)
        self.seats_listbox.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
        
        # Buttons
        btn_frame = tk.Frame(ticket_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="Refresh Shows", command=self.refresh_booking_shows).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Book Selected Seats", command=self.book_tickets, bg="green", fg="white").pack(side=tk.LEFT, padx=5)
        
        ticket_frame.grid_rowconfigure(1, weight=1)
        ticket_frame.grid_columnconfigure(1, weight=1)
        
        self.refresh_booking_shows()

    def refresh_booking_shows(self):
        for item in self.booking_shows_tree.get_children():
            self.booking_shows_tree.delete(item)
        
        shows = self.controller.get_all_shows()
        for show in shows:
            self.booking_shows_tree.insert('', tk.END, values=(
                show.id, show.film_name, show.cinema_name, 
                show.screen_number, show.show_date, show.show_time, 
                f"${show.base_price}"
            ))

    def on_show_select_for_booking(self, event):
        selected = self.booking_shows_tree.selection()
        if not selected:
            return
        
        show_id = self.booking_shows_tree.item(selected[0])['values'][0]
        screen_num = self.booking_shows_tree.item(selected[0])['values'][3]
        
        # Find screen_id from screen_num
        screens = self.controller.get_all_screens()
        screen_id = None
        for sc in screens:
            if sc.screen_number == screen_num:
                screen_id = sc.id
                break
        
        if screen_id:
            self.load_available_seats(show_id, screen_id)

    def load_available_seats(self, show_id, screen_id):
        self.seats_listbox.delete(0, tk.END)
        
        # Get all seats for this screen
        seats = self.controller.seat_repo.get_all_seats()
        screen_seats = [s for s in seats if s.screen_id == screen_id]
        
        # Get booked seats for this show
        booked_seats = self.controller.get_booked_seats_for_show(show_id)
        booked_seat_ids = {bs.seat_id for bs in booked_seats}
        
        # Show available seats
        for seat in screen_seats:
            if seat.id not in booked_seat_ids:
                self.seats_listbox.insert(tk.END, f"{seat.seat_number} ({seat.seat_type})")

    def book_tickets(self):
        selected_show = self.booking_shows_tree.selection()
        selected_seats = self.seats_listbox.curselection()
        
        if not selected_show:
            messagebox.showwarning("Warning", "Please select a show")
            return
        
        if not selected_seats:
            messagebox.showwarning("Warning", "Please select seats")
            return
        
        num_tickets = self.ticket_count.get()
        if len(selected_seats) != num_tickets:
            messagebox.showwarning("Warning", f"Please select exactly {num_tickets} seat(s)")
            return
        
        show_id = self.booking_shows_tree.item(selected_show[0])['values'][0]
        show_price = float(self.booking_shows_tree.item(selected_show[0])['values'][6].replace('$', ''))
        
        # Get selected seat details
        selected_seat_texts = [self.seats_listbox.get(i) for i in selected_seats]
        
        # Find screen_id for the show
        shows = self.controller.get_all_shows()
        show = next((s for s in shows if s.id == show_id), None)
        if not show:
            messagebox.showerror("Error", "Show not found")
            return
        
        screens = self.controller.get_all_screens()
        screen = next((s for s in screens if s.id == show.screen_id), None)
        if not screen:
            messagebox.showerror("Error", "Screen not found")
            return
        
        # Get seat objects
        all_seats = self.controller.seat_repo.get_all_seats()
        selected_seat_objects = []
        for seat_text in selected_seat_texts:
            seat_number = seat_text.split(' ')[0]
            seat = next((s for s in all_seats if s.screen_id == screen.id and s.seat_number == seat_number), None)
            if seat:
                selected_seat_objects.append(seat)
        
        if len(selected_seat_objects) != num_tickets:
            messagebox.showerror("Error", "Some seats could not be found")
            return
        
        # Confirm booking
        total_price = show_price * num_tickets
        seat_numbers = ', '.join([s.seat_number for s in selected_seat_objects])
        
        if not messagebox.askyesno("Confirm Booking", 
            f"Book {num_tickets} ticket(s) for seats: {seat_numbers}\nTotal: ${total_price}\n\nConfirm?"):
            return
        
        try:
            # Create booking
            import uuid
            from datetime import datetime
            booking_ref = str(uuid.uuid4())[:8].upper()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            from app.models.booking import Booking
            new_booking = Booking(None, booking_ref, self.user.user_id, show_id, None, total_price, 0.0, "CONFIRMED", now, now)
            booking_id = self.controller.add_booking(new_booking)
            
            # Add booked seats
            for seat in selected_seat_objects:
                self.controller.add_booked_seat(booking_id, show_id, seat.id)
            
            messagebox.showinfo("Success", f"Booking confirmed!\nReference: {booking_ref}\nSeats: {seat_numbers}")
            
            # Refresh views
            self.refresh_booking_shows()
            self.refresh_my_bookings()
            
        except Exception as e:
            messagebox.showerror("Error", f"Booking failed: {str(e)}")

    def setup_my_bookings_tab(self):
        tk.Label(self.my_bookings_frame, text="My Bookings", font=("Arial", 16, "bold")).pack(pady=10)
        
        cols = ('Reference', 'Movie', 'Cinema', 'Date', 'Time', 'Seats', 'Status', 'Total')
        self.my_bookings_tree = ttk.Treeview(self.my_bookings_frame, columns=cols, show='headings', height=15)
        for col in cols:
            self.my_bookings_tree.heading(col, text=col)
            self.my_bookings_tree.column(col, width=100)
        self.my_bookings_tree.pack(expand=True, fill='both', padx=10, pady=5)
        
        btn_frame = tk.Frame(self.my_bookings_frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Refresh Bookings", command=self.refresh_my_bookings).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel Booking", command=self.cancel_booking, bg="red", fg="white").pack(side=tk.LEFT, padx=5)
        
        self.refresh_my_bookings()

    def refresh_my_bookings(self):
        for item in self.my_bookings_tree.get_children():
            self.my_bookings_tree.delete(item)
        
        bookings = self.controller.get_bookings_by_user(self.user.user_id)
        for booking in bookings:
            # Get show details
            show = self.controller.get_show_by_id(booking.show_id)
            if show:
                # Get booked seats for this booking
                booked_seats = self.controller.get_booked_seats_for_booking(booking.id)
                seat_numbers = ', '.join([bs.seat_number for bs in booked_seats])
                
                self.my_bookings_tree.insert('', tk.END, values=(
                    booking.booking_reference, show.film_name, show.cinema_name,
                    show.show_date, show.show_time, seat_numbers, 
                    booking.status, f"${booking.total_amount}"
                ))

    def cancel_booking(self):
        selected = self.my_bookings_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a booking to cancel")
            return
        
        booking_ref = self.my_bookings_tree.item(selected[0])['values'][0]
        status = self.my_bookings_tree.item(selected[0])['values'][6]
        
        if status == "CANCELLED":
            messagebox.showwarning("Warning", "This booking is already cancelled")
            return
        
        if not messagebox.askyesno("Confirm Cancellation", f"Cancel booking {booking_ref}?\nThis action cannot be undone."):
            return
        
        try:
            self.controller.cancel_booking(booking_ref)
            messagebox.showinfo("Success", f"Booking {booking_ref} has been cancelled")
            self.refresh_my_bookings()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to cancel booking: {str(e)}")

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
