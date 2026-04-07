class Screen:
    def __init__(self, id, cinema_id, screen_number, total_seats, cinema_name=None):
        self.id = id
        self.cinema_id = cinema_id
        self.screen_number = screen_number
        self.total_seats = total_seats
        self.cinema_name = cinema_name

    def get_id(self):
        return self.id

    def get_cinema_id(self):
        return self.cinema_id

    def get_screen_number(self):
        return self.screen_number

    def get_total_seats(self):
        return self.total_seats

    def get_cinema_name(self):
        return self.cinema_name
