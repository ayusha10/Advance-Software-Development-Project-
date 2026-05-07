from app.repositories.user_repository import UserRepository
from app.repositories.cinema_repository import CinemaRepository
from app.repositories.screen_repository import ScreenRepository
from app.repositories.seat_repository import SeatRepository
from app.repositories.booking_repository import BookingRepository
from app.repositories.city_repository import CityRepository
from app.repositories.film_repository import FilmRepository
from app.repositories.show_repository import ShowRepository
from app.services.booking_service import BookingService

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
        self.booking_service = BookingService()

    # City Management
    def get_all_cities(self):
        return self.city_repo.get_all_cities()

    def add_city(self, city_name):
        return self.city_repo.add_city(city_name)

    def delete_city(self, city_id):
        self.city_repo.delete_city(city_id)

    def update_city(self, city_id, name):
        self.city_repo.update_city(city_id, name)

    # Film Management
    def get_all_films(self):
        return self.film_repo.get_all_films()

    def get_film_show_times(self):
        shows = self.show_repo.get_all_shows()
        show_times = {}
        for show in shows:
            show_times.setdefault(show.film_name, []).append(f"{show.show_date} {show.show_time}")
        return {name: ", ".join(times) for name, times in show_times.items()}

    def add_film(self, film):
        return self.film_repo.add_film(film)

    def delete_film(self, film_id):
        return self.film_repo.delete_film(film_id)

    def update_film(self, film):
        self.film_repo.update_film(film)

    # Show Management
    def get_all_shows(self, cinema_id=None):
        return self.show_repo.get_all_shows(cinema_id)

    def add_show(self, show):
        return self.show_repo.add_show(show)

    def delete_show(self, show_id):
        return self.show_repo.delete_show(show_id)

    def update_show(self, show):
        self.show_repo.update_show(show)

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

    def get_booking_by_ref(self, booking_ref):
        return self.booking_repo.get_booking_by_ref(booking_ref)

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

    # High-level booking flows using BookingService (enforces rules)
    def create_booking(self, user, show_id, seat_ids, customer_user_id=None, promo_code=None):
        return self.booking_service.create_booking(user, show_id, seat_ids, customer_user_id, promo_code)

    def cancel_booking_by_user(self, user, booking_ref, reason=None):
        return self.booking_service.cancel_booking(user, booking_ref, reason)

    # Seat Lock Management
    def lock_seats(self, show_id, seat_ids):
        """Lock seats for booking"""
        return self.booking_service.lock_seats(show_id, seat_ids)

    def unlock_seats(self, show_id, seat_ids):
        """Release seat locks"""
        return self.booking_service.unlock_seats(show_id, seat_ids)

    def get_locked_seats(self, show_id):
        """Get currently locked seats for a show"""
        return self.booking_service.get_seat_lock_status(show_id)

    # Admin Reports
    def get_bookings_per_listing(self):
        """Returns number of bookings for each film/show"""
        from config.database import get_connection
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                f.name AS film_name,
                s.show_date,
                s.show_time,
                sc.cinema_id,
                COUNT(DISTINCT b.id) AS booking_count,
                SUM(CASE WHEN b.status = 'CONFIRMED' THEN 1 ELSE 0 END) AS confirmed_count,
                SUM(CASE WHEN b.status = 'CANCELLED' THEN 1 ELSE 0 END) AS cancelled_count
            FROM shows s
            JOIN films f ON s.film_id = f.id
            JOIN screens sc ON s.screen_id = sc.id
            LEFT JOIN bookings b ON s.id = b.show_id
            GROUP BY s.id, f.name, s.show_date, s.show_time, sc.cinema_id
            ORDER BY f.name, s.show_date, s.show_time
        """)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def get_monthly_revenue_per_cinema(self, month=None, year=None):
        """Returns total monthly revenue per cinema. If month/year not provided, returns current month."""
        from datetime import date, datetime
        from config.database import get_connection
        
        if not month or not year:
            today = date.today()
            month = today.month
            year = today.year
        
        month_str = f"{year}-{month:02d}"
        
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                c.id,
                c.name AS cinema_name,
                ci.name AS city_name,
                COUNT(DISTINCT b.id) AS booking_count,
                SUM(CASE WHEN b.status = 'CONFIRMED' THEN b.total_price ELSE 0 END) AS total_revenue
            FROM cinemas c
            JOIN cities ci ON c.city_id = ci.id
            JOIN screens sc ON c.id = sc.cinema_id
            JOIN shows s ON sc.id = s.screen_id
            LEFT JOIN bookings b ON s.id = b.show_id
            WHERE b.booking_date IS NULL OR b.booking_date LIKE ?
            GROUP BY c.id, c.name, ci.name
            ORDER BY total_revenue DESC
        """, (month_str + '%',))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def get_top_revenue_film(self, month=None, year=None):
        """Returns the film with highest total revenue. If month/year not provided, returns all-time."""
        from datetime import date
        from config.database import get_connection
        
        conn = get_connection()
        cur = conn.cursor()
        
        if month and year:
            month_str = f"{year}-{month:02d}"
            cur.execute("""
                SELECT 
                    f.id,
                    f.name AS film_name,
                    COUNT(DISTINCT b.id) AS booking_count,
                    SUM(CASE WHEN b.status = 'CONFIRMED' THEN b.total_price ELSE 0 END) AS total_revenue
                FROM films f
                LEFT JOIN shows s ON f.id = s.film_id
                LEFT JOIN bookings b ON s.id = b.show_id
                WHERE b.booking_date IS NULL OR b.booking_date LIKE ?
                GROUP BY f.id, f.name
                ORDER BY total_revenue DESC
                LIMIT 1
            """, (month_str + '%',))
        else:
            cur.execute("""
                SELECT 
                    f.id,
                    f.name AS film_name,
                    COUNT(DISTINCT b.id) AS booking_count,
                    SUM(CASE WHEN b.status = 'CONFIRMED' THEN b.total_price ELSE 0 END) AS total_revenue
                FROM films f
                LEFT JOIN shows s ON f.id = s.film_id
                LEFT JOIN bookings b ON s.id = b.show_id
                GROUP BY f.id, f.name
                ORDER BY total_revenue DESC
                LIMIT 1
            """)
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result

    def get_monthly_staff_booking_counts(self, month=None, year=None):
        """Returns monthly staff booking counts sorted by count (descending)"""
        from datetime import date
        from config.database import get_connection
        
        if not month or not year:
            today = date.today()
            month = today.month
            year = today.year
        
        month_str = f"{year}-{month:02d}"
        
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                u.id,
                u.username,
                u.role,
                COUNT(b.id) AS booking_count,
                SUM(CASE WHEN b.status = 'CONFIRMED' THEN b.total_price ELSE 0 END) AS revenue_generated
            FROM users u
            LEFT JOIN bookings b ON u.id = b.user_id
            WHERE (u.role = 'Booking-Staff' OR u.role = 'Admin' OR u.role = 'Manager')
                AND (b.booking_date IS NULL OR b.booking_date LIKE ?)
            GROUP BY u.id, u.username, u.role
            ORDER BY booking_count DESC, u.username
        """, (month_str + '%',))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results
