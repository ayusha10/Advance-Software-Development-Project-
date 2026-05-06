import unittest
from tests.test_base import RepositoryTestCase
from app.repositories.user_repository import UserRepository
from app.repositories.show_repository import ShowRepository
from app.repositories.booking_repository import BookingRepository
from app.repositories.cinema_repository import CinemaRepository
from app.repositories.city_repository import CityRepository
from app.repositories.film_repository import FilmRepository
from app.repositories.screen_repository import ScreenRepository
from app.repositories.seat_repository import SeatRepository
from app.models.user import User
from app.models.booking import Booking
from app.models.cinema import Cinema
from app.models.city import City
from app.models.film import Film
from app.models.screen import Screen
from app.models.seat import Seat

class TestRepositories(RepositoryTestCase):
    # USER REPOSITORY TESTS
    def test_user_repository_add(self):
        repo = UserRepository()
        new_user = User(None, "newtester", "pass", "Customer")
        user_id = repo.add_user(new_user)
        self.assertIsNotNone(user_id)

    def test_user_repository_get_by_username(self):
        repo = UserRepository()
        new_user = User(None, "newtester2", "pass", "Customer")
        repo.add_user(new_user)
        fetched_user = repo.get_user_by_username("newtester2")
        self.assertEqual(fetched_user.username, "newtester2")

    def test_user_repository_get_all(self):
        repo = UserRepository()
        users = repo.get_all_users()
        self.assertIsNotNone(users)
        self.assertTrue(len(users) > 0)

    # CITY REPOSITORY TESTS
    def test_city_repository_add(self):
        city_repo = CityRepository()
        new_city = City(None, "Test City")
        city_id = city_repo.add_city(new_city)
        self.assertIsNotNone(city_id)

    def test_city_repository_get_all(self):
        city_repo = CityRepository()
        cities = city_repo.get_all_cities()
        self.assertIsNotNone(cities)
        self.assertTrue(len(cities) > 0)

    def test_city_repository_delete(self):
        city_repo = CityRepository()
        new_city = City(None, "Delete Test City")
        city_id = city_repo.add_city(new_city)
        city_repo.delete_city(city_id)
        # Verify deletion (try to get it)
        cities = city_repo.get_all_cities()
        city_names = [c.name for c in cities]
        self.assertNotIn("Delete Test City", city_names)

    # CINEMA REPOSITORY TESTS
    def test_cinema_repository_add(self):
        cinema_repo = CinemaRepository()
        new_cinema = Cinema(None, "Test Cinema", 1)
        cinema_id = cinema_repo.add_cinema(new_cinema)
        self.assertIsNotNone(cinema_id)

    def test_cinema_repository_get_all(self):
        cinema_repo = CinemaRepository()
        cinemas = cinema_repo.get_all_cinemas()
        self.assertIsNotNone(cinemas)
        self.assertTrue(len(cinemas) > 0)

    def test_cinema_repository_update(self):
        cinema_repo = CinemaRepository()
        new_cinema = Cinema(None, "Update Test Cinema", 1)
        cinema_id = cinema_repo.add_cinema(new_cinema)
        updated_cinema = Cinema(cinema_id, "Updated Cinema Name", 1)
        cinema_repo.update_cinema(updated_cinema)
        cinemas = cinema_repo.get_all_cinemas()
        cinema_names = [c.name for c in cinemas]
        self.assertIn("Updated Cinema Name", cinema_names)

    # FILM REPOSITORY TESTS
    def test_film_repository_add(self):
        film_repo = FilmRepository()
        new_film = Film(None, "Test Film", "Action", "PG", "Test description", 120)
        film_id = film_repo.add_film(new_film)
        self.assertIsNotNone(film_id)

    def test_film_repository_get_all(self):
        film_repo = FilmRepository()
        films = film_repo.get_all_films()
        self.assertIsNotNone(films)
        self.assertTrue(len(films) > 0)

    def test_film_repository_delete(self):
        film_repo = FilmRepository()
        new_film = Film(None, "Delete Test Film", "Drama", "R", "Description", 150)
        film_id = film_repo.add_film(new_film)
        film_repo.delete_film(film_id)
        # Verify deletion
        films = film_repo.get_all_films()
        film_names = [f.name for f in films]
        self.assertNotIn("Delete Test Film", film_names)

    # SCREEN REPOSITORY TESTS
    def test_screen_repository_add(self):
        screen_repo = ScreenRepository()
        new_screen = Screen(None, 1, 1, 100)  # cinema_id=1, screen_number=1, total_seats=100
        screen_id = screen_repo.add_screen(new_screen)
        self.assertIsNotNone(screen_id)

    def test_screen_repository_get_all(self):
        screen_repo = ScreenRepository()
        screens = screen_repo.get_all_screens()
        self.assertIsNotNone(screens)
        self.assertTrue(len(screens) > 0)

    def test_screen_repository_update(self):
        screen_repo = ScreenRepository()
        new_screen = Screen(None, 1, 5, 80)
        screen_id = screen_repo.add_screen(new_screen)
        updated_screen = Screen(screen_id, 1, 5, 90)
        screen_repo.update_screen(updated_screen)
        screens = screen_repo.get_all_screens()
        updated = [s for s in screens if s.id == screen_id]
        self.assertTrue(len(updated) > 0)

    # SEAT REPOSITORY TESTS
    def test_seat_repository_add(self):
        seat_repo = SeatRepository()
        new_seat = Seat(None, 2, "TESTSEAT001", "VIP")  # Use unique seat number to avoid constraint
        seat_id = seat_repo.add_seat(new_seat)
        self.assertIsNotNone(seat_id)

    def test_seat_repository_get_all(self):
        seat_repo = SeatRepository()
        seats = seat_repo.get_all_seats()
        self.assertIsNotNone(seats)
        self.assertTrue(len(seats) > 0)

    def test_seat_repository_delete(self):
        seat_repo = SeatRepository()
        new_seat = Seat(None, 1, "TEST1", "VIP")
        seat_id = seat_repo.add_seat(new_seat)
        seat_repo.delete_seat(seat_id)
        # Verify deletion
        seats = seat_repo.get_all_seats()
        seat_numbers = [s.seat_number for s in seats]
        self.assertNotIn("TEST1", seat_numbers)

    # BOOKING REPOSITORY TESTS
    def test_booking_repository_add(self):
        booking_repo = BookingRepository()
        new_booking = Booking(None, "TESTREF123", 1, 1, None, 20.0, 2.0, "CONFIRMED", "2026-05-06", "2026-05-06")
        booking_id = booking_repo.add_booking(new_booking)
        self.assertIsNotNone(booking_id)

    def test_booking_repository_get_all(self):
        booking_repo = BookingRepository()
        bookings = booking_repo.get_all_bookings()
        self.assertIsNotNone(bookings)
        # Note: May be empty if test database is fresh, so just verify it returns list
        self.assertIsInstance(bookings, list)

    def test_booking_repository_get_by_user(self):
        booking_repo = BookingRepository()
        bookings = booking_repo.get_bookings_by_user(1)
        self.assertIsNotNone(bookings)

    def test_show_repository_availability(self):
        show_repo = ShowRepository()
        booking_repo = BookingRepository()
        
        # Get a show
        shows = show_repo.get_all_shows()
        self.assertTrue(len(shows) > 0)
        show = shows[0]
        initial_available = show.available_seats
        
        # Create a booking
        booking = Booking(None, "TESTREF1", 1, show.id, None, 10.0, 0.0, "CONFIRMED", "2026-05-01", "2026-05-01")
        booking_id = booking_repo.add_booking(booking)
        
        # Add booked seat
        booking_repo.add_booked_seat(booking_id, show.id, 1)
        
        # Check availability decreased
        updated_show = show_repo.get_show_by_id(show.id)
        self.assertEqual(updated_show.available_seats, initial_available - 1)
        
        # Cancel booking
        booking_repo.cancel_booking("TESTREF1")
        
        # Check availability restored
        restored_show = show_repo.get_show_by_id(show.id)
        self.assertEqual(restored_show.available_seats, initial_available)

    def test_show_repository_get_all(self):
        show_repo = ShowRepository()
        shows = show_repo.get_all_shows()
        self.assertIsNotNone(shows)
        self.assertTrue(len(shows) > 0)

if __name__ == '__main__':
    unittest.main()
