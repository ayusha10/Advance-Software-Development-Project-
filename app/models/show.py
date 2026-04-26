class Show:
    def __init__(self, id, film_id, screen_id, show_date, show_time, base_price, film_name=None, cinema_name=None, screen_number=None):
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
