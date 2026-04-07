class Booking:
    def __init__(self, id, booking_ref, user_id, show_id, promo_id, total_price, service_fee, status, booking_date, created_at):
        self.id = id
        self.booking_ref = booking_ref
        self.user_id = user_id
        self.show_id = show_id
        self.promo_id = promo_id
        self.total_price = total_price
        self.service_fee = service_fee
        self.status = status
        self.booking_date = booking_date
        self.created_at = created_at

    def get_id(self):
        return self.id

    def get_booking_ref(self):
        return self.booking_ref

    def get_user_id(self):
        return self.user_id

    def get_show_id(self):
        return self.show_id

    def get_promo_id(self):
        return self.promo_id

    def get_total_price(self):
        return self.total_price

    def get_service_fee(self):
        return self.service_fee

    def get_status(self):
        return self.status

    def get_booking_date(self):
        return self.booking_date

    def get_created_at(self):
        return self.created_at
