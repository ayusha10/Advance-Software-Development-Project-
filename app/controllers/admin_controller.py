from app.repositories.user_repository import UserRepository
from app.repositories.cinema_repository import CinemaRepository
from app.repositories.screen_repository import ScreenRepository
from app.repositories.seat_repository import SeatRepository
from app.repositories.booking_repository import BookingRepository
from app.repositories.city_repository import CityRepository
from app.repositories.film_repository import FilmRepository
from app.repositories.show_repository import ShowRepository

class AdminController:
    def __init__(self):
        self.user_repo = UserRepository()
        self.cinema_repo = CinemaRepository()
        self.screen_repo = ScreenRepository()
        self.seat_repo = SeatRepository()
        self.booking_repo = BookingRepository()
        self.city_repo = CityRepository()
        self.film_repo = FilmRepository()
        self.show_repo = ShowRepository()

    # City Management
    def get_all_cities(self):
        return self.city_repo.get_all_cities()

    def add_city(self, city_name):
        return self.city_repo.add_city(city_name)

    def delete_city(self, city_id):
        self.city_repo.delete_city(city_id)

    # Film Management
    def get_all_films(self):
        return self.film_repo.get_all_films()

    def add_film(self, film):
        return self.film_repo.add_film(film)

    def delete_film(self, film_id):
        return self.film_repo.delete_film(film_id)

    # Show Management
    def get_all_shows(self, cinema_id=None):
        return self.show_repo.get_all_shows(cinema_id)

    def add_show(self, show):
        return self.show_repo.add_show(show)

    def delete_show(self, show_id):
        return self.show_repo.delete_show(show_id)

    # User & Registration
    def register_user(self, user):
        return self.user_repo.add_user(user)

    def get_all_users(self):
        return self.user_repo.get_all_users()

    def add_user(self, user):
        return self.user_repo.add_user(user)

    def update_user(self, user):
        self.user_repo.update_user(user)

    def delete_user(self, user_id):
        self.user_repo.delete_user(user_id)

    # Cinema Management
    def get_all_cinemas(self):
        return self.cinema_repo.get_all_cinemas()

    def add_cinema(self, cinema):
        return self.cinema_repo.add_cinema(cinema)

    def update_cinema(self, cinema):
        self.cinema_repo.update_cinema(cinema)

    def delete_cinema(self, cinema_id):
        self.cinema_repo.delete_cinema(cinema_id)

    # Screen Management
    def get_all_screens(self, cinema_id=None):
        return self.screen_repo.get_all_screens(cinema_id)

    def add_screen(self, screen):
        return self.screen_repo.add_screen(screen)

    def update_screen(self, screen):
        self.screen_repo.update_screen(screen)

    def delete_screen(self, screen_id):
        self.screen_repo.delete_screen(screen_id)

    # Seat Management
    def get_all_seats(self, screen_id=None):
        # We can add filtering to seat repo similarly if needed
        return self.seat_repo.get_all_seats()

    def add_seat(self, seat):
        return self.seat_repo.add_seat(seat)

    def update_seat(self, seat):
        self.seat_repo.update_seat(seat)

    def delete_seat(self, seat_id):
        self.seat_repo.delete_seat(seat_id)

    # Booking Management
    def get_all_bookings(self, cinema_id=None):
        return self.booking_repo.get_all_bookings(cinema_id)

    def add_booking(self, booking):
        return self.booking_repo.add_booking(booking)

    def update_booking(self, booking):
        self.booking_repo.update_booking(booking)

    def delete_booking(self, booking_id):
        self.booking_repo.delete_booking(booking_id)

    def get_bookings_by_user(self, user_id):
        return self.booking_repo.get_bookings_by_user(user_id)

    def get_show_by_id(self, show_id):
        return self.show_repo.get_show_by_id(show_id)

    def get_booked_seats_for_show(self, show_id):
        return self.booking_repo.get_booked_seats_for_show(show_id)

    def get_booked_seats_for_booking(self, booking_id):
        return self.booking_repo.get_booked_seats_for_booking(booking_id)

    def add_booked_seat(self, booking_id, show_id, seat_id):
        return self.booking_repo.add_booked_seat(booking_id, show_id, seat_id)

    def cancel_booking(self, booking_reference):
        return self.booking_repo.cancel_booking(booking_reference)
