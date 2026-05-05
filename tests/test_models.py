import unittest
from app.models.user import User
from app.models.booking import Booking
from app.models.film import Film
from app.models.show import Show

class TestModels(unittest.TestCase):
    def test_user_model(self):
        user = User(1, "testuser", "password123", "Customer")
        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.role, "Customer")
        self.assertTrue(user.can_book())
        self.assertFalse(user.is_admin())

    def test_film_model(self):
        film = Film(1, "Inception", "Sci-Fi", "PG-13", "A dream within a dream", 148)
        self.assertEqual(film.id, 1)
        self.assertEqual(film.name, "Inception")
        self.assertEqual(film.time_duration, 148)

    def test_show_model(self):
        show = Show(1, 1, 1, "2026-05-01", "18:00", 12.50, film_name="Inception")
        self.assertEqual(show.id, 1)
        self.assertEqual(show.base_price, 12.50)
        self.assertEqual(show.film_name, "Inception")

    def test_booking_model(self):
        booking = Booking(1, "REF123", 1, 1, None, 12.50, 0.0, "CONFIRMED", "2026-05-01", "2026-05-01")
        self.assertEqual(booking.id, 1)
        self.assertEqual(booking.booking_ref, "REF123")
        self.assertEqual(booking.status, "CONFIRMED")

if __name__ == '__main__':
    unittest.main()
