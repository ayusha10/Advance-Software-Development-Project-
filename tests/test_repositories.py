import unittest
from tests.test_base import RepositoryTestCase
from app.repositories.user_repository import UserRepository
from app.repositories.show_repository import ShowRepository
from app.repositories.booking_repository import BookingRepository
from app.models.user import User
from app.models.booking import Booking

class TestRepositories(RepositoryTestCase):
    def test_user_repository(self):
        repo = UserRepository()
        new_user = User(None, "newtester", "pass", "Customer")
        user_id = repo.add_user(new_user)
        self.assertIsNotNone(user_id)
        
        fetched_user = repo.get_user_by_username("newtester")
        self.assertEqual(fetched_user.username, "newtester")

    def test_show_repository_availability(self):
        show_repo = ShowRepository()
        booking_repo = BookingRepository()
        
        # Get a show (there are some pre-inserted from horizon_db.sql)
        shows = show_repo.get_all_shows()
        self.assertTrue(len(shows) > 0)
        show = shows[0]
        initial_available = show.available_seats
        
        # Create a booking for this show
        booking = Booking(None, "TESTREF1", 1, show.id, None, 10.0, 0.0, "CONFIRMED", "2026-05-01", "2026-05-01")
        booking_id = booking_repo.add_booking(booking)
        
        # Add a booked seat
        booking_repo.add_booked_seat(booking_id, show.id, 1) # Assuming seat 1 exists
        
        # Check available seats decreased
        updated_show = show_repo.get_show_by_id(show.id)
        self.assertEqual(updated_show.available_seats, initial_available - 1)
        
        # Cancel the booking
        booking_repo.cancel_booking("TESTREF1")
        
        # Check available seats increased back
        restored_show = show_repo.get_show_by_id(show.id)
        self.assertEqual(restored_show.available_seats, initial_available)

if __name__ == '__main__':
    unittest.main()
