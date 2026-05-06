class Show:
    def __init__(self, id, film_id, screen_id, show_date, show_time, base_price, film_name=None, cinema_name=None, screen_number=None, available_seats=0, lower_available=0, upper_available=0, vip_available=0):
        self.id = id
        self.film_id = film_id
        self.screen_id = screen_id
        self.show_date = show_date
        self.show_time = show_time
        self.base_price = base_price
        
        # Optional names for HUD/Display
        self.film_name = film_name
        self.cinema_name = cinema_name
        self.screen_number = screen_number
        self.available_seats = available_seats
        self.lower_available = lower_available
        self.upper_available = upper_available
        self.vip_available = vip_available

    def get_id(self):
        return self.id

    def get_film_id(self):
        return self.film_id

    def get_screen_id(self):
        return self.screen_id

    def get_show_time(self):
        return self.show_time

    def get_base_price(self):
        return self.base_price
    
    def get_display_info(self):
        return f"{self.film_name} | {self.cinema_name} - {self.screen_number} | {self.show_time}"

    # Pricing helpers
    def get_lower_price(self):
        """Lower hall base price (stored in show as base_price)."""
        return float(self.base_price)

    def get_upper_price(self):
        """Upper gallery price is 20% higher than lower hall."""
        return round(self.get_lower_price() * 1.2, 2)

    def get_vip_price(self):
        """VIP price is 20% higher than upper gallery."""
        return round(self.get_upper_price() * 1.2, 2)

    def price_for(self, seat_type, vip=False):
        """Return price for a given seat type. seat_type: 'lower' or 'upper'. vip: boolean for VIP seat."""
        st = seat_type.lower()
        if st == 'lower':
            price = self.get_lower_price()
        else:
            price = self.get_upper_price()
        if vip:
            price = round(price * 1.2, 2)
        return price

    # Seat distribution helper
    def compute_seat_distribution(self, total_seats):
        """Compute approximate counts for lower, upper and VIP seats.

        - Lower hall: ~30% of total seats (rounded)
        - Upper gallery: remaining seats
        - VIP seats: up to 10 seats in upper gallery
        Returns tuple: (lower_count, upper_count, vip_count)
        """
        lower = int(round(total_seats * 0.3))
        upper = total_seats - lower
        vip = min(10, upper)
        return lower, upper, vip
