class Seat:
    def __init__(self, id, screen_id, seat_number, seat_type, screen_info=None):
        self.id = id
        self.screen_id = screen_id
        self.seat_number = seat_number
        self.seat_type = seat_type
        self.screen_info = screen_info

    def get_id(self):
        return self.id

    def get_screen_id(self):
        return self.screen_id

    def get_seat_number(self):
        return self.seat_number

    def get_seat_type(self):
        return self.seat_type

    def get_screen_info(self):
        return self.screen_info
