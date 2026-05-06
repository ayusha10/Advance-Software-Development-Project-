import unittest
from app.models.user import User
from app.models.booking import Booking
from app.models.film import Film
from app.models.show import Show
from app.models.cinema import Cinema
from app.models.city import City
from app.models.screen import Screen
from app.models.seat import Seat

class TestModels(unittest.TestCase):
    # USER MODEL TESTS
    def test_user_model(self):
        user = User(1, "testuser", "password123", "Customer")
        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.role, "Customer")
        self.assertTrue(user.can_book())
        self.assertFalse(user.is_admin())

    def test_user_model_admin_role(self):
        admin = User(2, "admin", "adminpass", "Admin")
        self.assertTrue(admin.is_admin())
        self.assertFalse(admin.can_book())  # Admin cannot book (only Customer)

    def test_user_model_manager_role(self):
        manager = User(3, "manager", "managerpass", "Manager")
        self.assertTrue(manager.is_manager())
        self.assertFalse(manager.can_book())  # Manager cannot book (only Customer)

    # FILM MODEL TESTS
    def test_film_model(self):
        film = Film(1, "Inception", "Sci-Fi", "PG-13", "A dream within a dream", 148)
        self.assertEqual(film.id, 1)
        self.assertEqual(film.name, "Inception")
        self.assertEqual(film.genre, "Sci-Fi")
        self.assertEqual(film.age_rating, "PG-13")
        self.assertEqual(film.time_duration, 148)

    def test_film_model_different_genre(self):
        film = Film(2, "Titanic", "Romance", "PG", "A love story", 194)
        self.assertEqual(film.name, "Titanic")
        self.assertEqual(film.genre, "Romance")

    # SHOW MODEL TESTS
    def test_show_model(self):
        show = Show(1, 1, 1, "2026-05-01", "18:00", 12.50, film_name="Inception")
        self.assertEqual(show.id, 1)
        self.assertEqual(show.film_id, 1)
        self.assertEqual(show.screen_id, 1)
        self.assertEqual(show.base_price, 12.50)
        self.assertEqual(show.film_name, "Inception")

    def test_show_model_different_time(self):
        show = Show(2, 2, 2, "2026-05-02", "20:30", 15.00, film_name="Avatar")
        self.assertEqual(show.show_time, "20:30")
        self.assertEqual(show.base_price, 15.00)

    # BOOKING MODEL TESTS
    def test_booking_model(self):
        booking = Booking(1, "REF123", 1, 1, None, 12.50, 0.0, "CONFIRMED", "2026-05-01", "2026-05-01")
        self.assertEqual(booking.id, 1)
        self.assertEqual(booking.booking_ref, "REF123")
        self.assertEqual(booking.user_id, 1)
        self.assertEqual(booking.show_id, 1)
        self.assertEqual(booking.status, "CONFIRMED")
        self.assertEqual(booking.total_price, 12.50)

    def test_booking_model_with_promo(self):
        booking = Booking(2, "REF456", 2, 2, 1, 15.00, 2.0, "PENDING", "2026-05-02", "2026-05-02")
        self.assertEqual(booking.booking_ref, "REF456")
        self.assertIsNotNone(booking.promo_id)
        self.assertEqual(booking.service_fee, 2.0)

    # CINEMA MODEL TESTS
    def test_cinema_model(self):
        cinema = Cinema(1, "Cinema 1", 1, city_name="New York")
        self.assertEqual(cinema.id, 1)
        self.assertEqual(cinema.name, "Cinema 1")
        self.assertEqual(cinema.city_id, 1)
        self.assertEqual(cinema.city_name, "New York")

    def test_cinema_model_multiple(self):
        cinema2 = Cinema(2, "Cinema 2", 2, city_name="Los Angeles")
        self.assertEqual(cinema2.name, "Cinema 2")
        self.assertEqual(cinema2.city_name, "Los Angeles")

    # CITY MODEL TESTS
    def test_city_model(self):
        city = City(1, "New York")
        self.assertEqual(city.id, 1)
        self.assertEqual(city.name, "New York")

    def test_city_model_different_city(self):
        city = City(2, "Los Angeles")
        self.assertEqual(city.name, "Los Angeles")

    # SCREEN MODEL TESTS
    def test_screen_model(self):
        screen = Screen(1, 1, 1, 100, cinema_name="Cinema 1")
        self.assertEqual(screen.id, 1)
        self.assertEqual(screen.cinema_id, 1)
        self.assertEqual(screen.screen_number, 1)
        self.assertEqual(screen.total_seats, 100)
        self.assertEqual(screen.cinema_name, "Cinema 1")

    def test_screen_model_different_size(self):
        screen = Screen(2, 2, 2, 150, cinema_name="Cinema 2")
        self.assertEqual(screen.screen_number, 2)
        self.assertEqual(screen.total_seats, 150)

    # SEAT MODEL TESTS
    def test_seat_model(self):
        seat = Seat(1, 1, "A1", "Lower", screen_info="Screen 1")
        self.assertEqual(seat.id, 1)
        self.assertEqual(seat.screen_id, 1)
        self.assertEqual(seat.seat_number, "A1")
        self.assertEqual(seat.seat_type, "Lower")
        self.assertEqual(seat.screen_info, "Screen 1")

    def test_seat_model_vip(self):
        seat = Seat(2, 1, "VIP1", "VIP", screen_info="Screen 1")
        self.assertEqual(seat.seat_type, "VIP")
        self.assertEqual(seat.seat_number, "VIP1")

    def test_seat_model_upper(self):
        seat = Seat(3, 2, "B5", "Upper", screen_info="Screen 2")
        self.assertEqual(seat.seat_type, "Upper")
        self.assertEqual(seat.seat_number, "B5")

if __name__ == '__main__':
    unittest.main()
