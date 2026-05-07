import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.admin_controller import AdminController
from gui.theme import Theme

class AdminPanel:
    def __init__(self, user):
        self.user = user
        self.controller = AdminController()
        self.root = tk.Tk()
        self.root.title(f"Admin Dashboard - Welcome {user.username}")
        self.root.geometry("1100x800")
        
        # Apply Modern Theme
        Theme.apply(self.root)

        # Layout
        self.create_widgets()
        
        self.root.mainloop()

    def create_widgets(self):
        # Header with Logout
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill='x', padx=20, pady=20)
        
        ttk.Label(header_frame, text=f"HORIZON CINEMA ADMIN", style="Header.TLabel").pack(side=tk.LEFT)
        
        user_info = ttk.Frame(header_frame)
        user_info.pack(side=tk.RIGHT)
        ttk.Label(user_info, text=f"Logged in as: {self.user.username} ({self.user.role})", font=Theme.FONT_BOLD).pack(side=tk.LEFT, padx=10)
        if self.user.role == 'Manager':
            ttk.Button(user_info, text="Manager View", command=self.open_manager_view, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(user_info, text="Cancellation GUI", command=self.open_cancellation_gui, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(user_info, text="Logout", command=self.logout, style="Danger.TButton").pack(side=tk.LEFT)

        # Create Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Create Frames for each Tab
        self.user_frame = ttk.Frame(self.notebook)
        self.cinema_frame = ttk.Frame(self.notebook)
        self.screen_frame = ttk.Frame(self.notebook)
        self.seat_frame = ttk.Frame(self.notebook)
        self.booking_frame = ttk.Frame(self.notebook)
        self.book_tickets_frame = ttk.Frame(self.notebook)
        self.film_frame = ttk.Frame(self.notebook)
        self.city_frame = ttk.Frame(self.notebook)
        self.show_frame = ttk.Frame(self.notebook)
        self.reports_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.user_frame, text="User Management")
        self.notebook.add(self.cinema_frame, text="Cinema Management")
        self.notebook.add(self.screen_frame, text="Screen Management")
        self.notebook.add(self.seat_frame, text="Seat Management")
        self.notebook.add(self.book_tickets_frame, text="Book Tickets")
        self.notebook.add(self.booking_frame, text="Bookings")
        self.notebook.add(self.film_frame, text="Film Management")
        self.notebook.add(self.city_frame, text="City Management")
        self.notebook.add(self.show_frame, text="Show Management")
        self.notebook.add(self.reports_frame, text="Reports")

        # Initialize each tab
        self.setup_user_tab()
        self.setup_cinema_tab()
        self.setup_screen_tab()
        self.setup_seat_tab()
        self.setup_book_tickets_tab()
        self.setup_booking_tab()
        self.setup_film_tab()
        self.setup_city_tab()
        self.setup_show_tab()
        self.setup_reports_tab()

    def open_unified_booking_dialog_admin(self):
        """Single comprehensive admin booking form with scrollable sections"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Complete Booking Form - Admin")
        dialog.geometry("1200x900")
        Theme.apply(dialog)
        
        # Get customers
        users = self.controller.get_all_users()
        customer_list = [u for u in users if u.role == 'Customer']
        customer_map = {f"{u.username} (ID:{u.user_id})": u.user_id for u in customer_list}
        
        # STATE variables
        selected_show = [None]
        selected_customer_id = [None]
        
        # TITLE
        ttk.Label(dialog, text="HORIZON CINEMA - ADMIN BOOKING FORM", font=(Theme.FONT_FAMILY, 16, "bold")).pack(pady=10)
        
        # Create scrollable main frame
        main_container = ttk.Frame(dialog)
        main_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        canvas = tk.Canvas(main_container, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # SECTION 0: SELECT CUSTOMER
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(scrollable_frame, text="STEP 0: SELECT CUSTOMER", font=(Theme.FONT_FAMILY, 13, "bold")).pack(anchor='w', padx=15, pady=(10, 5))
        
        cust_frame = ttk.LabelFrame(scrollable_frame, text="Book For Customer", padding=15)
        cust_frame.pack(fill='x', padx=15, pady=5)
        
        ttk.Label(cust_frame, text="Select Customer:").pack(side=tk.LEFT, padx=5)
        cust_combo = ttk.Combobox(cust_frame, values=list(customer_map.keys()), state='readonly', width=45)
        cust_combo.pack(side=tk.LEFT, padx=10)
        
        def on_customer_select(event):
            cust_key = cust_combo.get()
            selected_customer_id[0] = customer_map.get(cust_key)
        
        cust_combo.bind('<<ComboboxSelected>>', on_customer_select)
        
        # SECTION 1: SELECT SHOW
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(scrollable_frame, text="STEP 1: SELECT MOVIE & SHOW", font=(Theme.FONT_FAMILY, 13, "bold")).pack(anchor='w', padx=15, pady=(10, 5))
        
        show_frame = ttk.LabelFrame(scrollable_frame, text="Available Shows", padding=15)
        show_frame.pack(fill='both', expand=False, padx=15, pady=5)
        
        cols = ('ID', 'Film', 'Cinema', 'Screen', 'Date', 'Time', 'Lower', 'Upper', 'VIP', 'Price')
        shows_tree = ttk.Treeview(show_frame, columns=cols, show='headings', height=5)
        for col in cols:
            shows_tree.heading(col, text=col, anchor='center')
            shows_tree.column(col, width=105, anchor='center')
        shows_tree.pack(fill='both', expand=True)
        
        def load_shows():
            shows_tree.delete(*shows_tree.get_children())
            shows = self.controller.get_all_shows()
            for show in shows:
                shows_tree.insert('', tk.END, values=(
                    show.id, show.film_name, show.cinema_name, show.screen_number,
                    show.show_date, show.show_time,
                    show.lower_available, show.upper_available, show.vip_available,
                    f"£{show.price_for('upper', False):.2f}"
                ))
        
        def on_show_select(event):
            sel = shows_tree.selection()
            if sel:
                values = shows_tree.item(sel[0])['values']
                selected_show[0] = {
                    'id': int(values[0]),
                    'film': values[1],
                    'cinema': values[2],
                    'screen': values[3],
                    'date': values[4],
                    'time': values[5],
                    'price': float(str(values[9]).replace('£', ''))
                }
                refresh_all_displays()
        
        shows_tree.bind('<<TreeviewSelect>>', on_show_select)
        load_shows()
        
        # SECTION 2: SHOW DETAILS
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(scrollable_frame, text="STEP 2: SHOW DETAILS", font=(Theme.FONT_FAMILY, 13, "bold")).pack(anchor='w', padx=15, pady=(10, 5))
        
        details_frame = ttk.LabelFrame(scrollable_frame, text="Selected Show Information", padding=15)
        details_frame.pack(fill='x', padx=15, pady=5)
        
        details_text = tk.Text(details_frame, height=5, wrap='word', bg='#f0f0f0')
        details_text.pack(fill='x')
        details_text.config(state='disabled')
        
        def update_details():
            details_text.config(state='normal')
            details_text.delete('1.0', tk.END)
            if selected_show[0]:
                info = f"""Film: {selected_show[0]['film']}
Cinema: {selected_show[0]['cinema']}
Screen: {selected_show[0]['screen']}
Date: {selected_show[0]['date']} at {selected_show[0]['time']}
Base Price per Ticket: £{selected_show[0]['price']:.2f}"""
                details_text.insert(tk.END, info)
            else:
                details_text.insert(tk.END, "No show selected. Please select a show above.")
            details_text.config(state='disabled')
        
        # SECTION 3: SEAT SELECTION
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(scrollable_frame, text="STEP 3: SELECT SEATS", font=(Theme.FONT_FAMILY, 13, "bold")).pack(anchor='w', padx=15, pady=(10, 5))
        
        seat_control_frame = ttk.Frame(scrollable_frame)
        seat_control_frame.pack(fill='x', padx=15, pady=5)
        
        ttk.Label(seat_control_frame, text="Seat Type Filter:").pack(side=tk.LEFT, padx=5)
        seat_type_var = tk.StringVar(value='All')
        seat_type_combo = ttk.Combobox(seat_control_frame, textvariable=seat_type_var, state='readonly', 
                                       values=['All', 'Lower', 'Upper', 'VIP'], width=12)
        seat_type_combo.pack(side=tk.LEFT, padx=5)
        
        seats_frame = ttk.LabelFrame(scrollable_frame, text="Available Seats (Select Multiple)", padding=15)
        seats_frame.pack(fill='both', expand=False, padx=15, pady=5)
        
        # Seats listbox with scrollbar
        seats_inner_frame = ttk.Frame(seats_frame)
        seats_inner_frame.pack(fill='both', expand=True)
        
        seats_listbox = tk.Listbox(seats_inner_frame, selectmode=tk.MULTIPLE, height=6, width=80)
        seats_listbox.pack(side=tk.LEFT, fill='both', expand=True)
        
        seats_scroll = ttk.Scrollbar(seats_inner_frame, orient='vertical', command=seats_listbox.yview)
        seats_scroll.pack(side=tk.RIGHT, fill='y')
        seats_listbox.config(yscrollcommand=seats_scroll.set)
        
        def refresh_available_seats():
            seats_listbox.delete(0, tk.END)
            if not selected_show[0]:
                return
            show_id = selected_show[0]['id']
            booking_service = self.controller.booking_service
            available = booking_service.get_available_seats_for_show(show_id)
            
            seat_type_filter = seat_type_var.get()
            for seat in sorted(available, key=lambda s: (s.seat_number)):
                seat_type = seat.get_seat_type()
                if seat_type_filter == 'All' or seat_type.lower() == seat_type_filter.lower():
                    price_mult = 1.0 if seat_type.lower() == 'lower' else 1.2 if seat_type.lower() == 'upper' else 1.44
                    seat_price = selected_show[0]['price'] * price_mult
                    seats_listbox.insert(tk.END, f"{seat.seat_number:>4} ({seat_type:<5})  £{seat_price:>6.2f}")
        
        seat_type_combo.bind('<<ComboboxSelected>>', lambda e: refresh_available_seats())
        
        # SECTION 4: PRICE CALCULATION
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(scrollable_frame, text="STEP 4: PRICE SUMMARY", font=(Theme.FONT_FAMILY, 13, "bold")).pack(anchor='w', padx=15, pady=(10, 5))
        
        price_frame = ttk.LabelFrame(scrollable_frame, text="Booking Cost Calculation", padding=15)
        price_frame.pack(fill='x', padx=15, pady=5)
        
        price_display = tk.StringVar(value="Select show and seats to calculate total price")
        price_label = ttk.Label(price_frame, textvariable=price_display, font=(Theme.FONT_FAMILY, 12, "bold"), foreground='#008000')
        price_label.pack(pady=10)
        
        def update_price_display():
            selected_indices = seats_listbox.curselection()
            if not selected_show[0] or not selected_indices:
                price_display.set("Select show and seats to calculate total price")
                return
            
            show_obj = next((s for s in self.controller.get_all_shows() if int(s.id) == selected_show[0]['id']), None)
            if not show_obj:
                return
            
            total = 0.0
            for idx in selected_indices:
                seat_text = seats_listbox.get(idx)
                seat_type = seat_text.split('(')[1].rstrip(')')
                price = show_obj.price_for(seat_type.lower(), vip=(seat_type.upper() == 'VIP'))
                total += float(price)
            
            num_seats = len(selected_indices)
            price_display.set(f"Total for {num_seats} ticket{'s' if num_seats != 1 else ''}: £{total:.2f}")
        
        seats_listbox.bind('<<ListboxSelect>>', lambda e: update_price_display())
        
        # SECTION 5: RECEIPT PREVIEW
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(scrollable_frame, text="STEP 5: BOOKING RECEIPT PREVIEW", font=(Theme.FONT_FAMILY, 13, "bold")).pack(anchor='w', padx=15, pady=(10, 5))
        
        receipt_frame = ttk.LabelFrame(scrollable_frame, text="Your Booking Receipt", padding=15)
        receipt_frame.pack(fill='both', expand=False, padx=15, pady=5)
        
        receipt_text = tk.Text(receipt_frame, height=8, wrap='word', bg='#fffacd', font=('Courier', 10))
        receipt_text.pack(fill='both', expand=True)
        receipt_text.config(state='disabled')
        
        def update_receipt():
            receipt_text.config(state='normal')
            receipt_text.delete('1.0', tk.END)
            
            if not selected_show[0]:
                receipt_text.insert(tk.END, "Select a show to preview receipt")
                receipt_text.config(state='disabled')
                return
            
            selected_indices = seats_listbox.curselection()
            if not selected_indices:
                receipt_text.insert(tk.END, "Select seats to preview receipt")
                receipt_text.config(state='disabled')
                return
            
            show_id = selected_show[0]['id']
            show_obj = next((s for s in self.controller.get_all_shows() if int(s.id) == show_id), None)
            
            seat_texts = [seats_listbox.get(i) for i in selected_indices]
            all_seats = self.controller.seat_repo.get_all_seats()
            screen_id = int(show_obj.screen_id)
            
            seat_numbers = []
            total_price = 0.0
            for seat_text in seat_texts:
                seat_num = seat_text.split()[0]
                seat_type = seat_text.split('(')[1].rstrip(')')
                seat_obj = next((s for s in all_seats if int(s.screen_id) == screen_id and s.seat_number == seat_num), None)
                
                if seat_obj:
                    seat_numbers.append(seat_num)
                    price = show_obj.price_for(seat_type.lower(), vip=(seat_type.upper() == 'VIP'))
                    total_price += float(price)
            
            cust_name = cust_combo.get().split('(')[0].strip() if cust_combo.get() else "TBD"
            
            from datetime import datetime
            receipt_lines = [
                "╔═══════════════════════════════════════════════╗",
                "║           HORIZON CINEMA BOOKING RECEIPT      ║",
                "╚═══════════════════════════════════════════════╝",
                "",
                f"Customer:           {cust_name}",
                f"Booking Reference:  [WILL BE GENERATED]",
                f"Film:               {show_obj.film_name}",
                f"Cinema:             {show_obj.cinema_name}",
                f"Screen:             {show_obj.screen_number}",
                f"Date:               {show_obj.show_date}",
                f"Time:               {show_obj.show_time}",
                f"Seats:              {', '.join(seat_numbers)}",
                f"Number of Tickets:  {len(seat_numbers)}",
                f"Total Cost:         £{total_price:.2f}",
                f"Booking Date:       {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                "",
                "╔═══════════════════════════════════════════════╗",
            ]
            
            receipt_text.insert(tk.END, '\n'.join(receipt_lines))
            receipt_text.config(state='disabled')
        
        def refresh_all_displays():
            update_details()
            update_price_display()
            refresh_available_seats()
            update_receipt()
        
        seats_listbox.bind('<<ListboxSelect>>', lambda e: [update_price_display(), update_receipt()])
        
        # BUTTONS
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill='x', pady=15, padx=15)
        
        def confirm_booking():
            if not selected_customer_id[0]:
                messagebox.showwarning("Warning", "Please select a customer")
                return
            
            selected_indices = seats_listbox.curselection()
            if not selected_show[0] or not selected_indices:
                messagebox.showwarning("Warning", "Please select a show and at least one seat")
                return
            
            show_id = selected_show[0]['id']
            show_obj = next((s for s in self.controller.get_all_shows() if int(s.id) == show_id), None)
            
            seat_texts = [seats_listbox.get(i) for i in selected_indices]
            all_seats = self.controller.seat_repo.get_all_seats()
            screen_id = int(show_obj.screen_id)
            
            seat_ids = []
            seat_numbers = []
            total_price = 0.0
            for seat_text in seat_texts:
                seat_num = seat_text.split()[0]
                seat_type = seat_text.split('(')[1].rstrip(')')
                seat_obj = next((s for s in all_seats if int(s.screen_id) == screen_id and s.seat_number == seat_num), None)
                
                if seat_obj:
                    seat_ids.append(seat_obj.id)
                    seat_numbers.append(seat_num)
                    price = show_obj.price_for(seat_type.lower(), vip=(seat_type.upper() == 'VIP'))
                    total_price += float(price)
            
            cust_name = cust_combo.get().split('(')[0].strip()
            
            if not messagebox.askyesno("Confirm Booking", 
                f"Confirm booking for {cust_name}?\n{len(seat_number)} seat(s): {', '.join(seat_numbers)}\nTotal: £{total_price:.2f}"):
                return
            
            try:
                receipt = self.controller.create_booking(self.user, show_id, seat_ids, customer_user_id=selected_customer_id[0])
                booking_ref = receipt.get('booking_ref')
                
                receipt_msg = f"""╔═══════════════════════════════════════════════╗
║        BOOKING CONFIRMED SUCCESSFULLY!       ║
╚═══════════════════════════════════════════════╝

Customer: {cust_name}
Booking Reference: {booking_ref}
Film: {receipt['film_name']}
Cinema: {show_obj.cinema_name}
Screen: {receipt['screen_number']}
Date: {receipt['film_date']}
Time: {receipt['show_time']}
Seats: {', '.join(receipt['seat_numbers'])}
Number of Tickets: {receipt['number_of_tickets']}
Total Cost: £{receipt['total_price']:.2f}
Booking Date: {receipt['created_at'][:10]}

Thank you for using Horizon Cinema Admin Panel!"""
                
                messagebox.showinfo("Booking Confirmed", receipt_msg)
                dialog.destroy()
                self.refresh_admin_booking_shows()
                self.refresh_bookings()
            except Exception as e:
                messagebox.showerror("Error", f"Booking failed: {str(e)}")
        
        ttk.Button(button_frame, text="✓ CONFIRM BOOKING", command=confirm_booking, style="Success.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="✕ CANCEL", command=dialog.destroy, style="Danger.TButton").pack(side=tk.LEFT, padx=5)
        
        # Initial load
        update_details()
        update_receipt()
        load_shows()
        
        # === SECTION 2: SHOW DETAILS ===
        ttk.Label(main_frame, text="2. SHOW DETAILS", font=(Theme.FONT_FAMILY, 12, "bold")).pack(anchor='w', pady=(10, 5))
        
        details_frame = ttk.LabelFrame(main_frame, text="Selected Show Info", padding=10)
        details_frame.pack(fill='x', pady=5)
        
        details_text = tk.Text(details_frame, height=3, wrap='word')
        details_text.pack(fill='x')
        details_text.config(state='disabled')
        
        def update_details():
            details_text.config(state='normal')
            details_text.delete('1.0', tk.END)
            if selected_show[0]:
                show_id, film, cinema, screen, date, time = selected_show[0]
                details_text.insert(tk.END, f"Film: {film}\nCinema: {cinema} | Screen: {screen} | Date: {date} at {time}")
            details_text.config(state='disabled')
        
        # === SECTION 3: SEAT TYPE & SELECTION ===
        ttk.Label(main_frame, text="3. SELECT SEATS", font=(Theme.FONT_FAMILY, 12, "bold")).pack(anchor='w', pady=(10, 5))
        
        seat_type_frame = ttk.Frame(main_frame)
        seat_type_frame.pack(fill='x', pady=5)
        
        ttk.Label(seat_type_frame, text="Seat Type:").pack(side=tk.LEFT, padx=5)
        seat_type_var = tk.StringVar(value='All')
        seat_type_combo = ttk.Combobox(seat_type_frame, textvariable=seat_type_var, state='readonly', values=['All', 'Lower', 'Upper', 'VIP'], width=15)
        seat_type_combo.pack(side=tk.LEFT, padx=5)
        
        seats_frame = ttk.LabelFrame(main_frame, text="Available Seats (select multiple)", padding=10)
        seats_frame.pack(fill='both', expand=True, pady=5)
        
        seats_listbox = tk.Listbox(seats_frame, selectmode=tk.MULTIPLE, height=5)
        seats_listbox.pack(fill='both', expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(seats_frame, orient='vertical', command=seats_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        seats_listbox.config(yscrollcommand=scrollbar.set)
        
        def refresh_available_seats():
            seats_listbox.delete(0, tk.END)
            if not selected_show[0]:
                return
            show_id = selected_show[0][0]
            booking_service = self.controller.booking_service
            available = booking_service.get_available_seats_for_show(show_id)
            
            seat_type_filter = seat_type_var.get()
            for seat in available:
                seat_type = seat.get_seat_type()
                if seat_type_filter == 'All' or seat_type.lower() == seat_type_filter.lower():
                    seats_listbox.insert(tk.END, f"{seat.seat_number} ({seat_type})")
        
        seat_type_combo.bind('<<ComboboxSelected>>', lambda e: refresh_available_seats())
        
        # === SECTION 4: PRICE CALCULATION ===
        ttk.Label(main_frame, text="4. PRICE SUMMARY", font=(Theme.FONT_FAMILY, 12, "bold")).pack(anchor='w', pady=(10, 5))
        
        price_frame = ttk.LabelFrame(main_frame, text="Total Cost", padding=10)
        price_frame.pack(fill='x', pady=5)
        
        price_display = tk.StringVar(value="Select show and seats to calculate price")
        ttk.Label(price_frame, textvariable=price_display, font=(Theme.FONT_FAMILY, 14, "bold"), foreground='green').pack()
        
        def update_price_display():
            selected_indices = seats_listbox.curselection()
            if not selected_show[0] or not selected_indices:
                price_display.set("Select show and seats to calculate price")
                return
            
            show_id = selected_show[0][0]
            show_obj = next((s for s in self.controller.get_all_shows() if int(s.id) == show_id), None)
            if not show_obj:
                return
            
            total = 0.0
            for idx in selected_indices:
                seat_text = seats_listbox.get(idx)
                seat_type = seat_text.split('(')[1].rstrip(')')
                price = show_obj.price_for(seat_type.lower(), vip=(seat_type.upper() == 'VIP'))
                total += float(price)
            
            price_display.set(f"Total: £{total:.2f} ({len(selected_indices)} ticket{'s' if len(selected_indices) != 1 else ''})")
        
        seats_listbox.bind('<<ListboxSelect>>', lambda e: update_price_display())
        
        # === SECTION 5: BOOKING RECEIPT ===
        ttk.Label(main_frame, text="5. BOOKING RECEIPT PREVIEW", font=(Theme.FONT_FAMILY, 12, "bold")).pack(anchor='w', pady=(10, 5))
        
        receipt_frame = ttk.LabelFrame(main_frame, text="Your Booking", padding=10)
        receipt_frame.pack(fill='both', expand=True, pady=5)
        
        receipt_text = tk.Text(receipt_frame, height=5, wrap='word')
        receipt_text.pack(fill='both', expand=True)
        receipt_text.config(state='disabled')
        
        def update_receipt():
            receipt_text.config(state='normal')
            receipt_text.delete('1.0', tk.END)
            
            if not selected_show[0]:
                receipt_text.insert(tk.END, "Select a show to preview receipt")
                receipt_text.config(state='disabled')
                return
            
            selected_indices = seats_listbox.curselection()
            if not selected_indices:
                receipt_text.insert(tk.END, "Select seats to preview receipt")
                receipt_text.config(state='disabled')
                return
            
            show_id = selected_show[0][0]
            show_obj = next((s for s in self.controller.get_all_shows() if int(s.id) == show_id), None)
            
            seat_texts = [seats_listbox.get(i) for i in selected_indices]
            all_seats = self.controller.seat_repo.get_all_seats()
            screen_id = int(show_obj.screen_id)
            
            seat_numbers = []
            total_price = 0.0
            for seat_text in seat_texts:
                seat_num = seat_text.split(' ')[0]
                seat_type = seat_text.split('(')[1].rstrip(')')
                seat_obj = next((s for s in all_seats if int(s.screen_id) == screen_id and s.seat_number == seat_num), None)
                
                if seat_obj:
                    seat_numbers.append(seat_num)
                    price = show_obj.price_for(seat_type.lower(), vip=(seat_type.upper() == 'VIP'))
                    total_price += float(price)
            
            from datetime import datetime
            receipt_lines = [
                "═══════════════════════════════════",
                "BOOKING RECEIPT",
                "═══════════════════════════════════",
                f"Booking Reference: [WILL BE GENERATED]",
                f"Film: {show_obj.film_name}",
                f"Film Date: {show_obj.show_date}",
                f"Show Time: {show_obj.show_time}",
                f"Cinema: {show_obj.cinema_name}",
                f"Screen: {show_obj.screen_number}",
                f"Seats: {', '.join(seat_numbers)}",
                f"Number of Tickets: {len(seat_numbers)}",
                f"Total Cost: £{total_price:.2f}",
                f"Booking Date: {datetime.now().strftime('%d/%m/%Y')}",
                "═══════════════════════════════════",
            ]
            
            receipt_text.insert(tk.END, '\n'.join(receipt_lines))
            receipt_text.config(state='disabled')
        
        seats_listbox.bind('<<ListboxSelect>>', lambda e: [update_details(), update_receipt()])
        
        # BUTTONS
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill='x', pady=10, padx=15)
        
        def confirm_booking():
            if not selected_customer_id[0]:
                messagebox.showwarning("Warning", "Please select a customer")
                return
            
            selected_indices = seats_listbox.curselection()
            if not selected_show[0] or not selected_indices:
                messagebox.showwarning("Warning", "Please select a show and at least one seat")
                return
            
            show_id = selected_show[0][0]
            show_obj = next((s for s in self.controller.get_all_shows() if int(s.id) == show_id), None)
            
            seat_texts = [seats_listbox.get(i) for i in selected_indices]
            all_seats = self.controller.seat_repo.get_all_seats()
            screen_id = int(show_obj.screen_id)
            
            seat_ids = []
            seat_numbers = []
            total_price = 0.0
            for seat_text in seat_texts:
                seat_num = seat_text.split(' ')[0]
                seat_type = seat_text.split('(')[1].rstrip(')')
                seat_obj = next((s for s in all_seats if int(s.screen_id) == screen_id and s.seat_number == seat_num), None)
                
                if seat_obj:
                    seat_ids.append(seat_obj.id)
                    seat_numbers.append(seat_num)
                    price = show_obj.price_for(seat_type.lower(), vip=(seat_type.upper() == 'VIP'))
                    total_price += float(price)
            
            cust_key = cust_combo.get()
            cust_username = cust_key.split(' ')[0]
            
            if not messagebox.askyesno("Confirm Booking", 
                f"Confirm booking for {cust_username}?\n{len(seat_numbers)} seat(s): {', '.join(seat_numbers)}\nTotal: £{total_price:.2f}"):
                return
            
            try:
                receipt = self.controller.create_booking(self.user, show_id, seat_ids, customer_user_id=selected_customer_id[0])
                booking_ref = receipt.get('booking_ref')
                
                receipt_msg = f"""BOOKING CONFIRMED!

Customer: {cust_username}
Booking Reference: {booking_ref}
Film: {receipt['film_name']}
Film Date: {receipt['film_date']}
Show Time: {receipt['show_time']}
Cinema: {show_obj.cinema_name}
Screen: {receipt['screen_number']}
Seats: {', '.join(receipt['seat_numbers'])}
Number of Tickets: {receipt['number_of_tickets']}
Total Cost: £{receipt['total_price']:.2f}
Booking Date: {receipt['created_at'][:10]}"""
                
                messagebox.showinfo("Success", receipt_msg)
                dialog.destroy()
                self.refresh_admin_booking_shows()
                self.refresh_bookings()
            except Exception as e:
                messagebox.showerror("Error", f"Booking failed: {str(e)}")
        
        ttk.Button(button_frame, text="Confirm Booking", command=confirm_booking, style="Success.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy, style="Danger.TButton").pack(side=tk.LEFT, padx=5)
        
        update_details()
        update_receipt()

    def logout(self):
        self.root.destroy()
        from gui.loginWindow import LoginWindow
        LoginWindow()

    def open_manager_view(self):
        self.root.destroy()
        from gui.manager_panal import ManagerPanel
        ManagerPanel(self.user)

    def open_cancellation_gui(self):
        from gui.cancellation_gui import CancellationWindow
        CancellationWindow(self.user)

    def setup_show_tab(self):
        ttk.Label(self.show_frame, text="Show Management", font=("Arial", 16, "bold")).pack(fill='x', pady=10)
        
        cols = ('ID', 'Film', 'Cinema', 'Screen', 'Time', 'Lower', 'Upper', 'VIP', 'Price')
        self.show_tree = ttk.Treeview(self.show_frame, columns=cols, show='headings')
        for col in cols:
            self.show_tree.heading(col, text=col, anchor='center')
            self.show_tree.column(col, width=100, anchor='center')
        self.show_tree.pack(expand=True, fill='both', padx=10, pady=10)

        btn_frame = ttk.Frame(self.show_frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_shows).pack(side=tk.LEFT, padx=5)
        if self.user.role == 'Manager':
            ttk.Button(btn_frame, text="Add Show", command=self.add_show_dialog).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="Edit Show", command=self.edit_show_dialog).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="Delete Show", command=self.delete_show).pack(side=tk.LEFT, padx=5)
        else:
            ttk.Label(btn_frame, text="(Show management is Manager-only)", foreground='gray').pack(side=tk.LEFT, padx=5)

        self.refresh_shows()

    def refresh_shows(self):
        for item in self.show_tree.get_children():
            self.show_tree.delete(item)
        shows = self.controller.get_all_shows()
        for s in shows:
            self.show_tree.insert('', tk.END, values=(
                s.id, s.film_name, s.cinema_name, s.screen_number, s.show_time, 
                s.lower_available, s.upper_available, s.vip_available, s.base_price
            ))

    def add_show_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Schedule New Show")
        dialog.geometry("500x700")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        # Film Selection
        ttk.Label(container, text="Select Film").pack(fill='x', pady=5)
        films = self.controller.get_all_films()
        film_map = {f.name: f.id for f in films}
        film_combo = ttk.Combobox(container, values=list(film_map.keys()), state="readonly")
        film_combo.pack(fill='x')

        # Screen Selection
        ttk.Label(container, text="Select Screen").pack(fill='x', pady=5)
        screens = self.controller.get_all_screens()
        screen_map = {f"{s.get_cinema_name()} - Screen {s.screen_number}": s.id for s in screens}
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
        screens = self.controller.get_all_screens()
        screen_map = {f"{s.get_cinema_name()} - Screen {s.screen_number}": s.id for s in screens}
        screen_combo = ttk.Combobox(container, values=list(screen_map.keys()), state="readonly")
        screen_combo.pack(fill='x')
        screen_label = f"{show.cinema_name} - Screen {show.screen_number}"
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



    def setup_city_tab(self):
        ttk.Label(self.city_frame, text="City Management", font=("Arial", 16, "bold")).pack(fill='x', pady=10)
        
        cols = ('ID', 'Name')
        self.city_tree = ttk.Treeview(self.city_frame, columns=cols, show='headings')
        for col in cols:
            self.city_tree.heading(col, text=col, anchor='center')
            self.city_tree.column(col, width=300, anchor='center')
        self.city_tree.pack(expand=True, fill='both', padx=10, pady=10)

        btn_frame = ttk.Frame(self.city_frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_cities).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add City", command=self.add_city_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete City", command=self.delete_city).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit City", command=self.edit_city_dialog).pack(side=tk.LEFT, padx=5)

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
        dialog.geometry("450x550")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="City Name").pack(fill='x', pady=5)
        name_entry = ttk.Entry(container)
        name_entry.pack(fill='x')

        def save_city():
            name = name_entry.get()
            if name:
                from app.models.city import City
                self.controller.add_city(name)
                self.refresh_cities()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "City name is required")

        ttk.Button(container, text="Save", command=save_city).pack(fill='x', pady=10)

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
        dialog.geometry("450x550")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="City Name").pack(fill='x', pady=5)
        name_entry = ttk.Entry(container)
        name_entry.insert(0, current_name)
        name_entry.pack(fill='x')

        def update_city():
            name = name_entry.get()
            if name:
                self.controller.update_city(city_id, name)
                self.refresh_cities()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "City name is required")

        ttk.Button(container, text="Update", command=update_city).pack(fill='x', pady=10)


    def setup_film_tab(self):
        ttk.Label(self.film_frame, text="Film Management", font=("Arial", 16, "bold")).pack(fill='x', pady=10)
        
        cols = ('ID', 'Name', 'Genre', 'Rating', 'Duration', 'Description', 'Actors', 'Show Times')
        self.film_tree = ttk.Treeview(self.film_frame, columns=cols, show='headings')
        for col in cols:
            self.film_tree.heading(col, text=col, anchor='center')
            if col in ('Description', 'Actors', 'Show Times'):
                self.film_tree.column(col, width=300, anchor='w')
            else:
                self.film_tree.column(col, width=100, anchor='center')
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
        show_times = self.controller.get_film_show_times()
        for f in films:
            self.film_tree.insert('', tk.END, values=(
                f.id,
                f.name,
                f.genre,
                f.age_rating,
                f.time_duration,
                f.description if f.description else '',
                f.actors if getattr(f, 'actors', None) else '',
                show_times.get(f.name, '')
            ))

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
        desc_text = tk.Text(container, height=3, width=30)
        desc_text.pack(fill='x')

        ttk.Label(container, text="Actors").pack(fill='x', pady=5)
        actors_entry = ttk.Entry(container, width=30)
        actors_entry.pack(fill='x')

        def save_film():
            name = name_entry.get()
            genre = genre_entry.get()
            rating = rating_entry.get()
            dur = dur_entry.get()
            desc = desc_text.get("1.0", tk.END).strip()
            actors = actors_entry.get().strip()
            if name and genre and dur and rating:
                try:
                    from app.models.film import Film
                    new_film = Film(None, name, genre, rating, desc, int(dur))
                    new_film.actors = actors
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
        desc_text = tk.Text(container, height=3, width=30)
        desc_text.insert("1.0", film.description or "")
        desc_text.pack(fill='x')

        ttk.Label(container, text="Actors").pack(fill='x', pady=5)
        actors_entry = ttk.Entry(container, width=30)
        actors_entry.insert(0, film.actors if getattr(film, 'actors', None) else "")
        actors_entry.pack(fill='x')

        def update_film():
            name = name_entry.get()
            genre = genre_entry.get()
            rating = rating_entry.get()
            dur = dur_entry.get()
            desc = desc_text.get("1.0", tk.END).strip()
            actors = actors_entry.get().strip()
            if name and genre and dur and rating:
                try:
                    from app.models.film import Film
                    updated_film = Film(film_id, name, genre, rating, desc, int(dur))
                    updated_film.actors = actors
                    self.controller.update_film(updated_film)
                    self.refresh_films()
                    dialog.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Duration must be an integer (e.g. 120)")
            else:
                messagebox.showwarning("Warning", "All fields except Description are required")

        ttk.Button(container, text="Update", command=update_film).pack(fill='x', pady=20)

    def setup_user_tab(self):
        ttk.Label(self.user_frame, text="User Management", font=("Arial", 16, "bold")).pack(fill='x', pady=10)
        
        # Table (Treeview)
        cols = ('ID', 'Username', 'Role', 'City', 'Created At')
        self.user_tree = ttk.Treeview(self.user_frame, columns=cols, show='headings')
        for col in cols:
            self.user_tree.heading(col, text=col, anchor='center')
            self.user_tree.column(col, width=150, anchor='center')
        self.user_tree.pack(expand=True, fill='both', padx=10, pady=10)

        # Buttons
        btn_frame = ttk.Frame(self.user_frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_users).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add User", command=self.add_user_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete User", command=self.delete_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit User", command=self.edit_user_dialog).pack(side=tk.LEFT, padx=5)

        self.refresh_users()

    def refresh_users(self):
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        users = self.controller.get_all_users()
        cities = self.controller.get_all_cities()
        city_map = {c.id: c.name for c in cities}

        for u in users:
            city_name = city_map.get(u.assigned_city_id, "N/A") if u.assigned_city_id else "N/A"
            self.user_tree.insert('', tk.END, values=(u.user_id, u.username, u.role, city_name, u.created_at))

    def add_user_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New User")
        dialog.geometry("450x550")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Username").pack(fill='x', pady=5)
        username_entry = ttk.Entry(container)
        username_entry.pack(fill='x')

        ttk.Label(container, text="Password").pack(fill='x', pady=5)
        password_entry = ttk.Entry(container, show="*")
        password_entry.pack(fill='x')

        ttk.Label(container, text="Role").pack(fill='x', pady=5)
        role_var = tk.StringVar(value="Admin")
        role_opt = ttk.OptionMenu(container, role_var, "Admin", "Admin", "Manager", "Booking-Staff", "Customer")
        role_opt.pack(fill='x')

        ttk.Label(container, text="City (For Managers)").pack(fill='x', pady=5)
        cities = self.controller.get_all_cities()
        city_map = {c.name: c.id for c in cities}
        city_combo = ttk.Combobox(container, values=list(city_map.keys()), state="readonly")
        city_combo.pack(fill='x')

        def save_user():
            username = username_entry.get()
            password = password_entry.get()
            role = role_var.get()
            city_name = city_combo.get()
            city_id = city_map.get(city_name) if role == "Manager" else None

            if username and password:
                if role == "Manager" and not city_id:
                    messagebox.showwarning("Warning", "City is required for Managers")
                    return
                from app.models.user import User
                new_user = User(None, username, password, role, None, assigned_city_id=city_id)
                self.controller.add_user(new_user)
                self.refresh_users()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "All fields are required")

        ttk.Button(container, text="Save", command=save_user).pack(fill='x', pady=20)

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
        dialog.geometry("450x550")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Username").pack(fill='x', pady=5)
        username_entry = ttk.Entry(container)
        username_entry.insert(0, current_username)
        username_entry.pack(fill='x')

        ttk.Label(container, text="Password (leave blank to keep current)").pack(fill='x', pady=5)
        password_entry = ttk.Entry(container, show="*")
        password_entry.pack(fill='x')

        ttk.Label(container, text="Role").pack(fill='x', pady=5)
        role_var = tk.StringVar(value=current_role)
        role_opt = ttk.OptionMenu(container, role_var, current_role, "Admin", "Manager", "Booking-Staff", "Customer")
        role_opt.pack(fill='x')

        ttk.Label(container, text="City (For Managers)").pack(fill='x', pady=5)
        cities = self.controller.get_all_cities()
        city_map = {c.name: c.id for c in cities}
        city_combo = ttk.Combobox(container, values=list(city_map.keys()), state="readonly")
        city_combo.pack(fill='x')
        
        # Pre-select city if user is a manager
        users = self.controller.get_all_users()
        target_user = next((u for u in users if u.user_id == user_id), None)
        if target_user and target_user.role == "Manager" and target_user.assigned_city_id:
            assigned_city = next((c.name for c in cities if c.id == target_user.assigned_city_id), None)
            if assigned_city:
                city_combo.set(assigned_city)

        def update_user():
            username = username_entry.get()
            password = password_entry.get()
            role = role_var.get()
            city_name = city_combo.get()
            city_id = city_map.get(city_name) if role == "Manager" else None

            if username:
                if role == "Manager" and not city_id:
                    messagebox.showwarning("Warning", "City is required for Managers")
                    return
                from app.models.user import User
                if not target_user:
                    messagebox.showerror("Error", "User not found")
                    return
                
                # If password is provided, we update it, else keep old
                new_pass = password if password else target_user.password
                
                updated_user = User(user_id, username, new_pass, role, target_user.created_at, assigned_city_id=city_id)
                self.controller.update_user(updated_user)
                self.refresh_users()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "Username is required")

        ttk.Button(container, text="Update", command=update_user).pack(fill='x', pady=20)


    # --- Stubs for other tabs ---
    def setup_cinema_tab(self):
        ttk.Label(self.cinema_frame, text="Cinema Management", font=("Arial", 16, "bold")).pack(fill='x', pady=10)
        
        # Table (Treeview)
        cols = ('ID', 'Name', 'City')
        self.cinema_tree = ttk.Treeview(self.cinema_frame, columns=cols, show='headings')
        for col in cols:
            self.cinema_tree.heading(col, text=col, anchor='center')
            self.cinema_tree.column(col, width=150, anchor='center')
        self.cinema_tree.pack(expand=True, fill='both', padx=10, pady=10)

        # Buttons - Manager can add/edit/delete, Admin view-only
        btn_frame = ttk.Frame(self.cinema_frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_cinemas).pack(side=tk.LEFT, padx=5)
        if self.user.role == 'Manager':
            ttk.Button(btn_frame, text="Add Cinema", command=self.add_cinema_dialog).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="Edit Cinema", command=self.edit_cinema_dialog).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="Delete Cinema", command=self.delete_cinema).pack(side=tk.LEFT, padx=5)
        else:
            ttk.Label(btn_frame, text="(Cinema management is Manager-only)", foreground='gray').pack(side=tk.LEFT, padx=5)

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
        dialog.geometry("450x550")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Name").pack(fill='x', pady=5)
        name_entry = ttk.Entry(container)
        name_entry.pack(fill='x')

        ttk.Label(container, text="City").pack(fill='x', pady=5)
        cities = self.controller.get_all_cities()
        city_names = [c.name for c in cities]
        city_map = {c.name: c.id for c in cities}
        
        city_combo = ttk.Combobox(container, values=city_names, state="readonly")
        city_combo.pack(fill='x')
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

        ttk.Button(container, text="Save", command=save_cinema).pack(fill='x', pady=20)

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
        dialog.geometry("450x550")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Name").pack(fill='x', pady=5)
        name_entry = ttk.Entry(container)
        name_entry.insert(0, current_name)
        name_entry.pack(fill='x')

        ttk.Label(container, text="City").pack(fill='x', pady=5)
        cities = self.controller.get_all_cities()
        city_names = [c.name for c in cities]
        city_map = {c.name: c.id for c in cities}
        
        city_combo = ttk.Combobox(container, values=city_names, state="readonly")
        city_combo.pack(fill='x')
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

        ttk.Button(container, text="Update", command=update_cinema).pack(fill='x', pady=20)



    def setup_screen_tab(self):
        ttk.Label(self.screen_frame, text="Screen Management", font=("Arial", 16, "bold")).pack(fill='x', pady=10)
        
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
        screens = self.controller.get_all_screens()
        for s in screens:
            self.screen_tree.insert('', tk.END, values=(s.id, s.get_cinema_name(), s.screen_number, s.total_seats))

    def add_screen_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Screen")
        dialog.geometry("450x550")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Cinema").pack(fill='x', pady=5)
        cinemas = self.controller.get_all_cinemas()
        cinema_names = [c.name for c in cinemas]
        cinema_map = {c.name: c.id for c in cinemas}
        
        cinema_combo = ttk.Combobox(container, values=cinema_names, state="readonly")
        cinema_combo.pack(fill='x')
        if cinema_names:
            cinema_combo.current(0)

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
        current_cinema = self.screen_tree.item(selected[0])['values'][1]
        current_num = self.screen_tree.item(selected[0])['values'][2]
        current_seats = self.screen_tree.item(selected[0])['values'][3]

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Screen")
        dialog.geometry("450x550")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Cinema").pack(fill='x', pady=5)
        cinemas = self.controller.get_all_cinemas()
        cinema_names = [c.name for c in cinemas]
        cinema_map = {c.name: c.id for c in cinemas}
        
        cinema_combo = ttk.Combobox(container, values=cinema_names, state="readonly")
        cinema_combo.pack(fill='x')
        if current_cinema in cinema_names:
            cinema_combo.set(current_cinema)
        elif cinema_names:
            cinema_combo.current(0)

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
                cinema_id_val = cinema_map[cinema_name]
                from app.models.screen import Screen
                updated_screen = Screen(screen_id, cinema_id_val, int(num), int(seats))
                self.controller.update_screen(updated_screen)
                self.refresh_screens()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "All fields are required")

        ttk.Button(container, text="Update", command=update_screen).pack(fill='x', pady=20)


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
        for s in seats:
            self.seat_tree.insert('', tk.END, values=(s.id, s.get_screen_info(), s.seat_number, s.seat_type))

    def add_seat_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Seat")
        dialog.geometry("450x550")
        container = ttk.Frame(dialog, padding=30)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Screen").pack(fill='x', pady=5)
        screens = self.controller.get_all_screens()
        cinemas = self.controller.get_all_cinemas()
        c_map = {c.id: c.name for c in cinemas}
        
        screen_labels = [f"{c_map.get(s.cinema_id, 'Unknown')} - Screen {s.screen_number}" for s in screens]
        screen_map = {f"{c_map.get(s.cinema_id, 'Unknown')} - Screen {s.screen_number}": s.id for s in screens}

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
                new_seat = Seat(None, screen_id, num, stype)
                self.controller.add_seat(new_seat)
                self.refresh_seats()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "All fields are required")

        ttk.Button(container, text="Save", command=save_seat).pack(fill='x', pady=20)
        
    def add_seat_button(self):
        """Alias for add_seat_dialog to ensure proper method availability"""
        self.add_seat_dialog()

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

        ttk.Label(container, text="Screen").pack(fill='x', pady=5)
        screens = self.controller.get_all_screens()
        cinemas = self.controller.get_all_cinemas()
        c_map = {c.id: c.name for c in cinemas}
        
        screen_labels = [f"{c_map.get(s.cinema_id, 'Unknown')} - Screen {s.screen_number}" for s in screens]
        screen_map = {f"{c_map.get(s.cinema_id, 'Unknown')} - Screen {s.screen_number}": s.id for s in screens}

        screen_combo = ttk.Combobox(container, values=screen_labels, state="readonly")
        screen_combo.pack(fill='x')
        if current_screen_info in screen_labels:
            screen_combo.set(current_screen_info)
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


    def setup_book_tickets_tab(self):
        header_frame = ttk.Frame(self.book_tickets_frame)
        header_frame.pack(fill='x', padx=10, pady=10)
        ttk.Label(header_frame, text="Book Tickets on Behalf of Customer", font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        ttk.Button(header_frame, text="📋 Complete Booking Form (All-in-One)", command=self.open_unified_booking_dialog_admin, style="Accent.TButton").pack(side=tk.RIGHT)

        cust_frame = ttk.Frame(self.book_tickets_frame)
        cust_frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(cust_frame, text="Select Customer:").pack(side=tk.LEFT)
        users = self.controller.get_all_users()
        customer_list = [u for u in users if u.role == 'Customer']
        self.admin_customer_map = {f"{u.username} (ID:{u.user_id})": u.user_id for u in customer_list}
        self.admin_customer_combo = ttk.Combobox(cust_frame, values=list(self.admin_customer_map.keys()), state='readonly', width=36)
        self.admin_customer_combo.pack(side=tk.LEFT, padx=10)

        show_frame = ttk.Frame(self.book_tickets_frame)
        show_frame.pack(fill='both', expand=True, padx=10, pady=5)

        cols = ('ID', 'Movie', 'Cinema', 'Screen', 'Date', 'Time', 'Lower', 'Upper', 'VIP', 'Price')
        self.admin_booking_shows_tree = ttk.Treeview(show_frame, columns=cols, show='headings', height=8)
        for col in cols:
            self.admin_booking_shows_tree.heading(col, text=col, anchor='center')
            self.admin_booking_shows_tree.column(col, width=90, anchor='center')
        self.admin_booking_shows_tree.pack(expand=True, fill='both')
        self.admin_booking_shows_tree.bind('<<TreeviewSelect>>', self.on_admin_show_select)

        seat_frame = ttk.LabelFrame(self.book_tickets_frame, text="Select Seats")
        seat_frame.pack(fill='both', expand=True, padx=10, pady=5)

        ttk.Label(seat_frame, text="Seat Type:").pack(anchor='w', padx=5, pady=(5, 0))
        self.admin_seat_type_filter = tk.StringVar(value='All')
        seat_type_combo = ttk.Combobox(seat_frame, textvariable=self.admin_seat_type_filter, state='readonly', values=['All', 'Lower', 'Upper', 'VIP'])
        seat_type_combo.pack(fill='x', padx=5, pady=5)
        seat_type_combo.bind('<<ComboboxSelected>>', self.refresh_admin_selected_show_seats)

        self.admin_seats_listbox = tk.Listbox(seat_frame, selectmode=tk.MULTIPLE, height=8)
        self.admin_seats_listbox.pack(side=tk.LEFT, fill='both', expand=True, padx=5, pady=5)

        right_panel = ttk.Frame(seat_frame)
        right_panel.pack(side=tk.LEFT, fill='y', padx=8)
        ttk.Label(right_panel, text="Tickets:").pack()
        self.admin_ticket_count = tk.IntVar(value=1)
        tk.Spinbox(right_panel, from_=1, to=12, textvariable=self.admin_ticket_count, width=5).pack(pady=6)
        ttk.Button(right_panel, text="Book for Customer", command=self.book_for_customer, style="Success.TButton").pack(pady=10)

        self.refresh_admin_booking_shows()

    def setup_booking_tab(self):
        ttk.Label(self.booking_frame, text="Bookings", font=("Arial", 16, "bold")).pack(fill='x', pady=10)

        cols = ('ID', 'Ref', 'User', 'Movie', 'Cinema', 'Seats', 'Price', 'Status', 'Date')
        self.booking_tree = ttk.Treeview(self.booking_frame, columns=cols, show='headings')
        for col in cols:
            self.booking_tree.heading(col, text=col, anchor='center')
            self.booking_tree.column(col, width=120, anchor='center')
        self.booking_tree.pack(expand=True, fill='both', padx=10, pady=10)
        self.booking_tree.bind('<<TreeviewSelect>>', self.on_booking_selected)

        btn_frame = ttk.Frame(self.booking_frame)
        btn_frame.pack(fill='x', pady=5, padx=10)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_bookings).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel Booking", command=self.cancel_booking).pack(side=tk.LEFT, padx=5)

        details_frame = ttk.LabelFrame(self.booking_frame, text="Booking Details")
        details_frame.pack(fill='x', padx=10, pady=10)
        self.booking_details = tk.Text(details_frame, height=8, wrap='word')
        self.booking_details.pack(fill='x', padx=8, pady=8)
        self.booking_details.configure(state='disabled')

        self.refresh_bookings()

    def refresh_admin_booking_shows(self):
        for item in self.admin_booking_shows_tree.get_children():
            self.admin_booking_shows_tree.delete(item)

        try:
            shows = self.controller.get_all_shows()
            if not shows:
                return  # No shows available
            
            for show in shows:
                self.admin_booking_shows_tree.insert('', tk.END, values=(
                    show.id, show.film_name, show.cinema_name,
                    show.screen_number, show.show_date, show.show_time,
                    show.lower_available, show.upper_available, show.vip_available,
                    f"£{show.base_price:.2f}"
                ))
        except Exception as e:
            pass  # Silently fail on refresh

    def on_admin_show_select(self, event):
        selected = self.admin_booking_shows_tree.selection()
        if not selected:
            return

        item_values = self.admin_booking_shows_tree.item(selected[0])['values']
        show_id = int(item_values[0])
        show = self.controller.get_show_by_id(show_id)
        if show:
            self.load_admin_available_seats(show_id, show.screen_id)

    def refresh_admin_selected_show_seats(self, event=None):
        selected = self.admin_booking_shows_tree.selection()
        if not selected:
            return

        item_values = self.admin_booking_shows_tree.item(selected[0])['values']
        show_id = int(item_values[0])
        show = self.controller.get_show_by_id(show_id)
        if show:
            self.load_admin_available_seats(show_id, show.screen_id)

    def load_admin_available_seats(self, show_id, screen_id):
        self.admin_seats_listbox.delete(0, tk.END)

        seats = self.controller.seat_repo.get_all_seats()
        screen_seats = [s for s in seats if int(s.screen_id) == int(screen_id)]
        booked = self.controller.get_booked_seats_for_show(show_id)
        booked_ids = {b['seat_id'] for b in booked}

        locked_seats = self.controller.get_locked_seats(show_id)
        locked_ids = {ls[0] for ls in locked_seats}

        unavailable_ids = booked_ids | locked_ids

        for seat in screen_seats:
            if seat.id not in unavailable_ids:
                seat_type_filter = self.admin_seat_type_filter.get()
                if seat_type_filter == 'All' or seat.seat_type == seat_type_filter:
                    self.admin_seats_listbox.insert(tk.END, f"{seat.seat_number} ({seat.seat_type})|ID:{seat.id}")

    def book_for_customer(self):
        customer_label = self.admin_customer_combo.get()
        if not customer_label:
            messagebox.showwarning("Warning", "Select a customer to book for")
            return

        customer_id = self.admin_customer_map.get(customer_label)

        selected_show = self.admin_booking_shows_tree.selection()
        if not selected_show:
            messagebox.showwarning("Warning", "Select a show")
            return

        show_id = int(self.admin_booking_shows_tree.item(selected_show[0])['values'][0])

        selected_indices = self.admin_seats_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Select seats")
            return

        if len(selected_indices) != self.admin_ticket_count.get():
            messagebox.showwarning("Warning", f"Please select exactly {self.admin_ticket_count.get()} seats")
            return

        seat_texts = [self.admin_seats_listbox.get(i) for i in selected_indices]
        seat_ids = [int(txt.split('|ID:')[-1]) for txt in seat_texts]

        try:
            receipt = self.controller.create_booking(self.user, show_id, seat_ids, customer_user_id=customer_id)
            booking_ref = receipt.get('booking_ref')
            film_date = receipt.get('film_date')
            total_price = receipt.get('total_price')
            receipt_text = (
                f"Booked For: {customer_label}\n"
                f"Processed By: {self.user.username}\n"
                f"Reference: {booking_ref}\n"
                f"Film: {receipt.get('film_name')}\n"
                f"Film Date: {film_date}\n"
                f"Show Time: {receipt.get('show_time')}\n"
                f"Screen #: {receipt.get('screen_number')}\n"
                f"Tickets: {receipt.get('number_of_tickets')}\n"
                f"Seats: {', '.join(receipt.get('seat_numbers', []))}\n"
                f"Booking Date: {receipt.get('booking_date')}\n"
                f"Total: £{total_price}"
            )
            messagebox.showinfo("Success", receipt_text)
            self.refresh_admin_booking_shows()
            self.refresh_bookings()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create booking: {str(e)}")

    def refresh_bookings(self):
        for item in self.booking_tree.get_children():
            self.booking_tree.delete(item)
        bookings = self.controller.get_all_bookings()
        for b in bookings:
            self.booking_tree.insert('', tk.END, values=(
                b.id, b.booking_ref, b.username, b.movie_name, b.cinema_name, b.seats, b.total_price, b.status, b.booking_date
            ))
        self._write_booking_details("Select a booking to view its details.")

    def on_booking_selected(self, event):
        selected = self.booking_tree.selection()
        if not selected:
            return

        values = self.booking_tree.item(selected[0])['values']
        if not values:
            return

        booking_id = values[0]
        booking_ref = values[1]
        customer_name = values[2]
        movie_name = values[3]
        cinema_name = values[4]
        seats = values[5]
        total_price = values[6]
        status = values[7]
        booking_date = values[8]

        booking = next((item for item in self.controller.get_all_bookings() if item.id == booking_id), None)
        show_time = 'Unknown'
        if booking:
            show = self.controller.get_show_by_id(booking.show_id)
            if show:
                show_time = show.show_time

        details = [
            f"Booking Ref: {booking_ref}",
            f"Customer: {customer_name}",
            f"Movie: {movie_name}",
            f"Cinema: {cinema_name}",
            f"Show Time: {show_time}",
            f"Seats: {seats}",
            f"Status: {status}",
            f"Booking Date: {booking_date}",
            f"Total: {total_price}",
        ]
        self._write_booking_details("\n".join(details))

    def _write_booking_details(self, text):
        if not hasattr(self, 'booking_details'):
            return
        self.booking_details.configure(state='normal')
        self.booking_details.delete('1.0', tk.END)
        self.booking_details.insert(tk.END, text)
        self.booking_details.configure(state='disabled')

    def cancel_booking(self):
        selected = self.booking_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a booking first")
            return
        booking_ref = self.booking_tree.item(selected[0])['values'][1]
        if messagebox.askyesno("Confirm", f"Cancel booking {booking_ref}?"):
            try:
                result = self.controller.cancel_booking_by_user(self.user, booking_ref)
                refund = result.get('refund_amount') if isinstance(result, dict) else None
                msg = f"Booking {booking_ref} has been cancelled"
                if refund is not None:
                    msg += f"\nRefund amount: £{refund}"
                messagebox.showinfo("Success", msg)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to cancel booking: {str(e)}")
            self.refresh_shows()
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

    def setup_reports_tab(self):
        ttk.Label(self.reports_frame, text="Admin Reports", font=("Arial", 16, "bold")).pack(fill='x', pady=10)
        
        # Report selection
        control_frame = ttk.Frame(self.reports_frame)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(control_frame, text="Select Report:").pack(side=tk.LEFT, padx=5)
        report_var = tk.StringVar(value="bookings_per_listing")
        report_combo = ttk.Combobox(control_frame, textvariable=report_var, 
            values=["bookings_per_listing", "monthly_revenue", "top_film", "staff_bookings"],
            state="readonly", width=30)
        report_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Generate Report", 
                   command=lambda: self.generate_report(report_var.get())).pack(side=tk.LEFT, padx=5)
        
        # Report output
        self.report_text = tk.Text(self.reports_frame, height=30, width=120, wrap='word')
        self.report_text.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Initial report
        self.generate_report("bookings_per_listing")

    def generate_report(self, report_type):
        self.report_text.delete('1.0', tk.END)
        
        try:
            if report_type == "bookings_per_listing":
                self.generate_bookings_per_listing_report()
            elif report_type == "monthly_revenue":
                self.generate_monthly_revenue_report()
            elif report_type == "top_film":
                self.generate_top_film_report()
            elif report_type == "staff_bookings":
                self.generate_staff_bookings_report()
        except Exception as e:
            self.report_text.insert(tk.END, f"Error generating report: {str(e)}")

    def generate_bookings_per_listing_report(self):
        report = "=" * 120 + "\n"
        report += "BOOKINGS PER LISTING REPORT\n"
        report += "=" * 120 + "\n\n"
        
        try:
            results = self.controller.get_bookings_per_listing()
            if not results:
                report += "No bookings found in the system.\n"
            else:
                report += f"{'Film Name':<30} {'Date':<12} {'Time':<10} {'Total':<8} {'Confirmed':<10} {'Cancelled':<10}\n"
                report += "-" * 120 + "\n"
                
                for row in results:
                    film_name, show_date, show_time, cinema_id, booking_count, confirmed_count, cancelled_count = row
                    report += f"{film_name:<30} {show_date:<12} {show_time:<10} {booking_count:<8} {confirmed_count if confirmed_count else 0:<10} {cancelled_count if cancelled_count else 0:<10}\n"
        except Exception as e:
            report += f"Error generating report: {str(e)}\n"
        
        self.report_text.insert(tk.END, report)

    def generate_monthly_revenue_report(self):
        report = "=" * 100 + "\n"
        report += "MONTHLY REVENUE REPORT\n"
        report += "=" * 100 + "\n\n"
        
        try:
            results = self.controller.get_monthly_revenue_per_cinema()
            if not results:
                report += "No revenue data found in the system.\n"
            else:
                report += f"{'Cinema Name':<30} {'City':<15} {'Bookings':<12} {'Revenue':<15}\n"
                report += "-" * 100 + "\n"
                
                total_revenue = 0.0
                total_bookings = 0
                for row in results:
                    cinema_id, cinema_name, city_name, booking_count, revenue = row
                    revenue = revenue if revenue else 0.0
                    total_revenue += revenue
                    total_bookings += booking_count
                    report += f"{cinema_name:<30} {city_name:<15} {booking_count:<12} £{revenue:<14.2f}\n"
                
                report += "-" * 100 + "\n"
                report += f"{'TOTAL':<30} {'':<15} {total_bookings:<12} £{total_revenue:<14.2f}\n"
        except Exception as e:
            report += f"Error generating report: {str(e)}\n"
        
        self.report_text.insert(tk.END, report)

    def generate_top_film_report(self):
        report = "=" * 80 + "\n"
        report += "TOP REVENUE-GENERATING FILM\n"
        report += "=" * 80 + "\n\n"
        
        try:
            result = self.controller.get_top_revenue_film()
            if result:
                film_id, film_name, booking_count, total_revenue = result
                revenue = total_revenue if total_revenue else 0.0
                report += f"Film Name: {film_name}\n"
                report += f"Total Bookings: {booking_count}\n"
                report += f"Total Revenue: £{revenue:.2f}\n"
            else:
                report += "No bookings found in the system.\n"
        except Exception as e:
            report += f"Error generating report: {str(e)}\n"
        
        self.report_text.insert(tk.END, report)

    def generate_staff_bookings_report(self):
        report = "=" * 100 + "\n"
        report += "MONTHLY STAFF BOOKING COUNTS\n"
        report += "=" * 100 + "\n\n"
        
        try:
            results = self.controller.get_monthly_staff_booking_counts()
            if not results:
                report += "No staff booking data found in the system.\n"
            else:
                report += f"{'Staff Name':<25} {'Role':<15} {'Bookings':<12} {'Revenue Generated':<15}\n"
                report += "-" * 100 + "\n"
                
                for row in results:
                    user_id, username, role, booking_count, revenue = row
                    revenue = revenue if revenue else 0.0
                    report += f"{username:<25} {role:<15} {booking_count:<12} £{revenue:<14.2f}\n"
        except Exception as e:
            report += f"Error generating report: {str(e)}\n"
        
        self.report_text.insert(tk.END, report)


if __name__ == "__main__":
    # Test
    from app.models.user import User
    AdminPanel(User(1, 'admin_test', 'pass', 'Admin', 'none'))
