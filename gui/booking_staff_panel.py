import tkinter as tk
from tkinter import ttk, messagebox
from gui.theme import Theme
from app.controllers.admin_controller import AdminController

class BookingStaffPanel:
    def __init__(self, user):
        self.user = user
        self.controller = AdminController()
        self.root = tk.Tk()
        self.root.title(f"Booking Staff Panel - {user.username}")
        self.root.geometry("1000x700")
        Theme.apply(self.root)

        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        header = ttk.Frame(self.root)
        header.pack(fill='x', padx=20, pady=10)
        ttk.Label(header, text="HORIZON CINEMA - Booking Desk", style="Header.TLabel").pack(side=tk.LEFT)
        user_info = ttk.Frame(header)
        user_info.pack(side=tk.RIGHT)
        ttk.Label(user_info, text=f"Staff: {self.user.username}", font=Theme.FONT_BOLD).pack(side=tk.LEFT, padx=8)
        ttk.Button(user_info, text="Logout", command=self.logout, style="Danger.TButton").pack(side=tk.LEFT)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        self.book_frame = ttk.Frame(self.notebook)
        self.my_bookings_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.book_frame, text="Book Tickets")
        self.notebook.add(self.my_bookings_frame, text="Bookings - City")

        self.setup_book_tab()
        self.setup_my_bookings_tab()

    def setup_book_tab(self):
        ttk.Label(self.book_frame, text="Book Tickets on Behalf of Customer", font=("Arial", 14, "bold")).pack(fill='x', pady=8)

        # Customer selection
        cust_frame = ttk.Frame(self.book_frame)
        cust_frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(cust_frame, text="Select Customer:").pack(side=tk.LEFT)
        users = self.controller.get_all_users()
        customer_list = [u for u in users if u.role == 'Customer']
        self.customer_map = {f"{u.username} (ID:{u.user_id})": u.user_id for u in customer_list}
        self.customer_combo = ttk.Combobox(cust_frame, values=list(self.customer_map.keys()), state='readonly')
        self.customer_combo.pack(side=tk.LEFT, padx=10)

        # Shows list (filtered by staff assigned city)
        show_frame = ttk.Frame(self.book_frame)
        show_frame.pack(fill='both', expand=True, padx=10, pady=10)

        cols = ('ID', 'Movie', 'Cinema', 'Screen', 'Date', 'Time', 'Lower', 'Upper', 'VIP', 'Price')
        self.shows_tree = ttk.Treeview(show_frame, columns=cols, show='headings', height=8)
        for col in cols:
            self.shows_tree.heading(col, text=col, anchor='center')
            self.shows_tree.column(col, width=90, anchor='center')
        self.shows_tree.pack(expand=True, fill='both')
        self.shows_tree.bind('<<TreeviewSelect>>', self.on_show_select)

        btns = ttk.Frame(self.book_frame)
        btns.pack(fill='x', padx=10, pady=6)
        ttk.Button(btns, text="Refresh Shows", command=self.refresh_shows).pack(side=tk.LEFT, padx=5)

        # Seats & booking
        seat_frame = ttk.LabelFrame(self.book_frame, text="Select Seats")
        seat_frame.pack(fill='both', expand=True, padx=10, pady=6)
        self.seats_listbox = tk.Listbox(seat_frame, selectmode=tk.MULTIPLE, height=8)
        self.seats_listbox.pack(side=tk.LEFT, fill='both', expand=True, padx=5, pady=5)

        right_panel = ttk.Frame(seat_frame)
        right_panel.pack(side=tk.LEFT, fill='y', padx=8)
        ttk.Label(right_panel, text="Tickets:").pack()
        self.ticket_count = tk.IntVar(value=1)
        tk_spin = tk.Spinbox(right_panel, from_=1, to=12, textvariable=self.ticket_count, width=5)
        tk_spin.pack(pady=6)
        ttk.Button(right_panel, text="Book for Customer", command=self.book_for_customer, style="Success.TButton").pack(pady=10)

        self.refresh_shows()

    def refresh_shows(self):
        for item in self.shows_tree.get_children():
            self.shows_tree.delete(item)
        # Filter shows by staff assigned city
        staff_city = getattr(self.user, 'assigned_city_id', None)
        shows = self.controller.get_all_shows()
        cinemas = self.controller.get_all_cinemas()
        screens = self.controller.get_all_screens()
        # map cinema id -> city_id
        cinema_city = {c.id: c.city_id for c in cinemas}
        screen_map = {s.id: s for s in screens}

        for s in shows:
            screen = screen_map.get(s.screen_id)
            if not screen:
                continue
            cinema_id = screen.cinema_id
            if staff_city and cinema_city.get(cinema_id) != staff_city:
                continue
            self.shows_tree.insert('', tk.END, values=(
                s.id, s.film_name, s.cinema_name, s.screen_number, s.show_date, s.show_time,
                s.lower_available, s.upper_available, s.vip_available, f"£{s.base_price}"
            ))

    def on_show_select(self, event):
        sel = self.shows_tree.selection()
        if not sel:
            return
        vals = self.shows_tree.item(sel[0])['values']
        show_id = int(vals[0])
        # find screen id via show repository
        show = self.controller.get_show_by_id(show_id)
        if not show:
            return
        screen_id = show.screen_id
        self.load_available_seats(show_id, screen_id)

    def load_available_seats(self, show_id, screen_id):
        self.seats_listbox.delete(0, tk.END)
        seats = self.controller.seat_repo.get_all_seats()
        screen_seats = [s for s in seats if int(s.screen_id) == int(screen_id)]
        booked = self.controller.get_booked_seats_for_show(show_id)
        booked_ids = {b['seat_id'] for b in booked}
        for s in screen_seats:
            if s.id not in booked_ids:
                self.seats_listbox.insert(tk.END, f"{s.seat_number} ({s.seat_type})|ID:{s.id}")

    def book_for_customer(self):
        cust_label = self.customer_combo.get()
        if not cust_label:
            messagebox.showwarning("Warning", "Select a customer to book for")
            return
        customer_id = self.customer_map.get(cust_label)

        sel = self.shows_tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a show")
            return
        show_id = int(self.shows_tree.item(sel[0])['values'][0])

        selected_indices = self.seats_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Select seats")
            return
        if len(selected_indices) != self.ticket_count.get():
            messagebox.showwarning("Warning", f"Please select exactly {self.ticket_count.get()} seats")
            return

        seat_texts = [self.seats_listbox.get(i) for i in selected_indices]
        seat_ids = [int(txt.split('|ID:')[-1]) for txt in seat_texts]

        try:
            receipt = self.controller.create_booking(self.user, show_id, seat_ids, customer_user_id=customer_id)
            booking_ref = receipt.get('booking_ref')
            messagebox.showinfo("Success", f"Booking created for {cust_label}\nReference: {booking_ref}\nTotal: £{receipt.get('total_price')}")
            self.refresh_shows()
            self.refresh_bookings()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create booking: {str(e)}")

    # Bookings tab
    def setup_my_bookings_tab(self):
        ttk.Label(self.my_bookings_frame, text="Bookings in Assigned City", font=("Arial", 14, "bold")).pack(fill='x', pady=8)
        cols = ('ID', 'Ref', 'User', 'Movie', 'Cinema', 'Seats', 'Price', 'Status', 'Date')
        self.book_tree = ttk.Treeview(self.my_bookings_frame, columns=cols, show='headings')
        for col in cols:
            self.book_tree.heading(col, text=col, anchor='center')
            self.book_tree.column(col, width=110, anchor='center')
        self.book_tree.pack(expand=True, fill='both', padx=10, pady=10)

        btns = ttk.Frame(self.my_bookings_frame)
        btns.pack(fill='x', padx=10)
        ttk.Button(btns, text="Refresh", command=self.refresh_bookings).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="Cancel Booking", command=self.cancel_selected_booking).pack(side=tk.LEFT, padx=5)

        self.refresh_bookings()

    def refresh_bookings(self):
        for it in self.book_tree.get_children():
            self.book_tree.delete(it)
        # aggregate bookings for cinemas in staff city
        staff_city = getattr(self.user, 'assigned_city_id', None)
        cinemas = self.controller.get_all_cinemas()
        target_cinemas = [c.id for c in cinemas if c.city_id == staff_city]
        bookings = []
        for cid in target_cinemas:
            bookings.extend(self.controller.get_all_bookings(cid))
        for b in bookings:
            self.book_tree.insert('', tk.END, values=(b.id, b.booking_ref, b.username, b.movie_name, b.cinema_name, b.seats, b.total_price, b.status, b.booking_date))

    def cancel_selected_booking(self):
        sel = self.book_tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a booking")
            return
        booking_ref = self.book_tree.item(sel[0])['values'][1]
        if not messagebox.askyesno("Confirm", f"Cancel booking {booking_ref}?"):
            return
        try:
            result = self.controller.cancel_booking_by_user(self.user, booking_ref)
            refund = result.get('refund_amount') if isinstance(result, dict) else None
            msg = f"Booking {booking_ref} cancelled"
            if refund is not None:
                msg += f"\nRefund: £{refund}"
            messagebox.showinfo("Success", msg)
            self.refresh_shows()
            self.refresh_bookings()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to cancel booking: {str(e)}")

    def logout(self):
        self.root.destroy()
        from gui.loginWindow import LoginWindow
        LoginWindow()

if __name__ == '__main__':
    # quick local test stub
    from app.models.user import User
    BookingStaffPanel(User(3, 'staff26', 'pass', 'Booking-Staff', None, assigned_city_id=1))
