import tkinter as tk
from tkinter import ttk, messagebox

from gui.theme import Theme
from app.controllers.admin_controller import AdminController


class CancellationWindow:
    def __init__(self, user):
        self.user = user
        self.controller = AdminController()
        self._lookup_after_id = None
        self._selected_booking_ref = None
        self.root = tk.Toplevel()
        self.root.title("Cancellation GUI")
        self.root.geometry("1120x620")
        Theme.apply(self.root)
        self._build_ui()

    def _build_ui(self):
        container = ttk.Frame(self.root, padding=24)
        container.pack(expand=True, fill='both')

        ttk.Label(container, text="Cancel Booking", style="Header.TLabel").pack(anchor='w', pady=(0, 12))
        ttk.Label(container, text="Select a booking from the list or enter a booking reference to look it up and cancel it if allowed.").pack(anchor='w', pady=(0, 16))

        main = ttk.Frame(container)
        main.pack(expand=True, fill='both')

        left = ttk.Frame(main)
        left.pack(side=tk.LEFT, fill='both', expand=False, padx=(0, 16))

        form = ttk.Frame(left)
        form.pack(fill='x', pady=(0, 16))

        ttk.Label(form, text="Booking Reference").grid(row=0, column=0, sticky='w', pady=4)
        self.ref_var = tk.StringVar()
        self.ref_entry = ttk.Entry(form, textvariable=self.ref_var)
        self.ref_entry.grid(row=0, column=1, sticky='ew', padx=(12, 0), pady=4)
        self.ref_entry.bind('<Return>', lambda event: self.lookup_booking())
        self.ref_var.trace_add('write', self._schedule_lookup)

        ttk.Label(form, text="Reason").grid(row=1, column=0, sticky='w', pady=4)
        self.reason_entry = ttk.Entry(form)
        self.reason_entry.grid(row=1, column=1, sticky='ew', padx=(12, 0), pady=4)

        form.columnconfigure(1, weight=1)

        actions = ttk.Frame(left)
        actions.pack(fill='x', pady=(0, 16))
        ttk.Button(actions, text="Lookup", command=self.lookup_booking).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(actions, text="Cancel Booking", command=self.cancel_booking, style="Danger.TButton").pack(side=tk.LEFT)
        ttk.Button(actions, text="Refresh List", command=self.refresh_booking_list).pack(side=tk.LEFT, padx=8)

        ttk.Label(left, text="Available Bookings").pack(anchor='w', pady=(0, 6))
        cols = ('Ref', 'Movie', 'Cinema', 'Date', 'Time', 'Status', 'Total')
        self.booking_tree = ttk.Treeview(left, columns=cols, show='headings', height=16)
        for col in cols:
            self.booking_tree.heading(col, text=col, anchor='center')
            self.booking_tree.column(col, width=130, anchor='center')
        self.booking_tree.pack(fill='both', expand=True)
        self.booking_tree.bind('<<TreeviewSelect>>', self.on_booking_selected)

        right = ttk.Frame(main)
        right.pack(side=tk.LEFT, fill='both', expand=True)

        self.details = tk.Text(right, height=22, wrap='word')
        self.details.pack(expand=True, fill='both')
        self.details.configure(state='disabled')

        self.refresh_booking_list()

    def _schedule_lookup(self, *args):
        if self._lookup_after_id is not None:
            self.root.after_cancel(self._lookup_after_id)
        self._lookup_after_id = self.root.after(350, self.lookup_booking)

    def _get_visible_bookings(self):
        if self.user.role == 'Customer':
            return self.controller.get_bookings_by_user(self.user.user_id)

        if self.user.role == 'Booking-Staff' and getattr(self.user, 'assigned_city_id', None):
            cinemas = [c.id for c in self.controller.get_all_cinemas() if c.city_id == self.user.assigned_city_id]
            bookings = []
            seen = set()
            for cinema_id in cinemas:
                for booking in self.controller.get_all_bookings(cinema_id):
                    if booking.booking_ref not in seen:
                        bookings.append(booking)
                        seen.add(booking.booking_ref)
            return bookings

        return self.controller.get_all_bookings()

    def refresh_booking_list(self):
        if not hasattr(self, 'booking_tree'):
            return
        for item in self.booking_tree.get_children():
            self.booking_tree.delete(item)
        for booking in self._get_visible_bookings():
            self.booking_tree.insert(
                '',
                tk.END,
                values=(
                    booking.booking_ref,
                    booking.movie_name or 'Unknown',
                    booking.cinema_name or 'Unknown',
                    booking.booking_date,
                    getattr(self.controller.get_show_by_id(booking.get_show_id()), 'show_time', 'Unknown'),
                    booking.status,
                    f'£{booking.total_price}',
                ),
            )

    def on_booking_selected(self, event):
        selected = self.booking_tree.selection()
        if not selected:
            return
        values = self.booking_tree.item(selected[0])['values']
        booking_ref = str(values[0])
        self._selected_booking_ref = booking_ref
        self.ref_var.set(booking_ref)
        self.lookup_booking()

    def lookup_booking(self):
        booking_ref = self.ref_entry.get().strip().upper()
        if not booking_ref:
            messagebox.showwarning("Warning", "Enter a booking reference")
            self._write_details("")
            return

        if len(booking_ref) < 8:
            self._write_details("Enter the full booking reference to load details.")
            return

        booking = self.controller.get_booking_by_ref(booking_ref)
        if not booking:
            matches = [b for b in self._get_visible_bookings() if b.booking_ref.upper().startswith(booking_ref)]
            if len(matches) == 1:
                booking = matches[0]
                booking_ref = booking.booking_ref
                self.ref_var.set(booking_ref)
            elif len(matches) > 1:
                self._write_details(
                    "Multiple bookings match that reference prefix. Select one from the list on the left."
                )
                return
            else:
                self._write_details(f"Booking {booking_ref} not found.")
                return

        show = self.controller.get_show_by_id(booking.get_show_id())
        lines = [
            f"Booking Ref: {booking.booking_ref}",
            f"Status: {booking.status}",
            f"Customer User ID: {booking.user_id}",
            f"Film: {show.film_name if show else 'Unknown'}",
            f"Cinema: {show.cinema_name if show else 'Unknown'}",
            f"Screen: {show.screen_number if show else 'Unknown'}",
            f"Date: {booking.booking_date}",
            f"Show Time: {show.show_time if show else 'Unknown'}",
            f"Total Price: £{booking.total_price}",
        ]
        self._write_details("\n".join(lines))

    def cancel_booking(self):
        booking_ref = self.ref_entry.get().strip().upper()
        if not booking_ref and self._selected_booking_ref:
            booking_ref = self._selected_booking_ref
        reason = self.reason_entry.get().strip() or None
        if not booking_ref:
            messagebox.showwarning("Warning", "Enter a booking reference")
            return

        if not messagebox.askyesno("Confirm Cancellation", f"Cancel booking {booking_ref}?"):
            return

        try:
            result = self.controller.cancel_booking_by_user(self.user, booking_ref, reason)
            refund = result.get('refund_amount') if isinstance(result, dict) else None
            msg = f"Booking {booking_ref} cancelled successfully."
            if refund is not None:
                msg += f"\nRefund amount: £{refund}"
            messagebox.showinfo("Success", msg)
            self.lookup_booking()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _write_details(self, text):
        self.details.configure(state='normal')
        self.details.delete('1.0', tk.END)
        self.details.insert(tk.END, text)
        self.details.configure(state='disabled')
