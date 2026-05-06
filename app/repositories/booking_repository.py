from config.database import get_connection
import app.models.booking

class BookingRepository:
    def get_all_bookings(self, cinema_id=None):
        connection = get_connection()
        connection.row_factory = __import__('sqlite3').Row
        cursor = connection.cursor()
        base_query = """
            SELECT b.*, f.name as movie_name, c.name as cinema_name, u.username,
            (SELECT GROUP_CONCAT(s.seat_number) FROM booked_seats bs JOIN seats s ON bs.seat_id = s.id WHERE bs.booking_id = b.id) as seats
            FROM bookings b
            JOIN users u ON b.user_id = u.id
            JOIN shows sh ON b.show_id = sh.id
            JOIN films f ON sh.film_id = f.id
            JOIN screens sc ON sh.screen_id = sc.id
            JOIN cinemas c ON sc.cinema_id = c.id
        """
        if cinema_id:
            query = base_query + " WHERE sc.cinema_id = ?"
            cursor.execute(query, (cinema_id,))
        else:
            query = base_query
            cursor.execute(query)
        results = cursor.fetchall()

        bookings = []
        for result in results:
            result = dict(result)
            bookings.append(app.models.booking.Booking(
                id=result['id'],
                booking_ref=result['booking_ref'],
                user_id=result['user_id'],
                show_id=result['show_id'],
                promo_id=result['promo_id'],
                total_price=result['total_price'],
                service_fee=result['service_fee'],
                status=result['status'],
                booking_date=result['booking_date'],
                created_at=result['created_at'],
                movie_name=result['movie_name'],
                cinema_name=result['cinema_name'],
                username=result['username'],
                seats=result['seats']
            ))
        cursor.close()
        connection.close()
        return bookings

    def add_booking(self, booking):
        connection = get_connection()
        cursor = connection.cursor()
        query = """INSERT INTO bookings (booking_ref, user_id, show_id, promo_id, total_price, service_fee, status, booking_date) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        cursor.execute(query, (booking.booking_ref, booking.user_id, booking.show_id, booking.promo_id, 
                               booking.total_price, booking.service_fee, booking.status, booking.booking_date))
        connection.commit()
        booking_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return booking_id

    def update_booking(self, booking):
        connection = get_connection()
        cursor = connection.cursor()
        query = """UPDATE bookings SET booking_ref = ?, user_id = ?, show_id = ?, promo_id = ?, 
                   total_price = ?, service_fee = ?, status = ?, booking_date = ? WHERE id = ?"""
        cursor.execute(query, (booking.booking_ref, booking.user_id, booking.show_id, booking.promo_id, 
                               booking.total_price, booking.service_fee, booking.status, booking.booking_date, booking.id))
        connection.commit()
        cursor.close()
        connection.close()

    def delete_booking(self, booking_id):
        connection = get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM bookings WHERE id = ?"
        cursor.execute(query, (booking_id,))
        connection.commit()
        cursor.close()
        connection.close()

    def get_bookings_by_user(self, user_id):
        connection = get_connection()
        connection.row_factory = __import__('sqlite3').Row
        cursor = connection.cursor()
        query = """
            SELECT b.*, f.name as movie_name, c.name as cinema_name, u.username,
            (SELECT GROUP_CONCAT(s.seat_number) FROM booked_seats bs JOIN seats s ON bs.seat_id = s.id WHERE bs.booking_id = b.id) as seats
            FROM bookings b
            JOIN users u ON b.user_id = u.id
            JOIN shows sh ON b.show_id = sh.id
            JOIN films f ON sh.film_id = f.id
            JOIN screens sc ON sh.screen_id = sc.id
            JOIN cinemas c ON sc.cinema_id = c.id
            WHERE b.user_id = ?
        """
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()

        bookings = []
        for result in results:
            result = dict(result)
            bookings.append(app.models.booking.Booking(
                id=result['id'],
                booking_ref=result['booking_ref'],
                user_id=result['user_id'],
                show_id=result['show_id'],
                promo_id=result['promo_id'],
                total_price=result['total_price'],
                service_fee=result['service_fee'],
                status=result['status'],
                booking_date=result['booking_date'],
                created_at=result['created_at'],
                movie_name=result['movie_name'],
                cinema_name=result['cinema_name'],
                username=result['username'],
                seats=result['seats']
            ))
        cursor.close()
        connection.close()
        return bookings

    def get_booked_seats_for_show(self, show_id):
        connection = get_connection()
        connection.row_factory = __import__('sqlite3').Row
        cursor = connection.cursor()
        query = """
            SELECT bs.*, s.seat_number 
            FROM booked_seats bs
            JOIN seats s ON bs.seat_id = s.id
            JOIN bookings b ON bs.booking_id = b.id
            WHERE bs.show_id = ? AND b.status != 'CANCELLED'
        """
        cursor.execute(query, (show_id,))
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results

    def get_booked_seats_for_booking(self, booking_id):
        connection = get_connection()
        connection.row_factory = __import__('sqlite3').Row
        cursor = connection.cursor()
        query = """
            SELECT bs.*, s.seat_number 
            FROM booked_seats bs
            JOIN seats s ON bs.seat_id = s.id
            WHERE bs.booking_id = ?
        """
        cursor.execute(query, (booking_id,))
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results

    def add_booked_seat(self, booking_id, show_id, seat_id):
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO booked_seats (booking_id, show_id, seat_id) VALUES (?, ?, ?)"
        cursor.execute(query, (booking_id, show_id, seat_id))
        connection.commit()
        cursor.close()
        connection.close()

    def cancel_booking(self, booking_reference):
        connection = get_connection()
        cursor = connection.cursor()
        query = "UPDATE bookings SET status = 'CANCELLED' WHERE booking_ref = ?"
        cursor.execute(query, (booking_reference,))
        connection.commit()
        cursor.close()
        connection.close()

    def delete_booked_seats_by_booking(self, booking_id):
        connection = get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM booked_seats WHERE booking_id = ?"
        cursor.execute(query, (booking_id,))
        connection.commit()
        cursor.close()
        connection.close()

    def get_booking_by_ref(self, booking_ref):
        connection = get_connection()
        connection.row_factory = __import__('sqlite3').Row
        cursor = connection.cursor()
        query = "SELECT * FROM bookings WHERE booking_ref = ?"
        cursor.execute(query, (booking_ref,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            r = dict(result)
            return app.models.booking.Booking(
                id=r['id'],
                booking_ref=r['booking_ref'],
                user_id=r['user_id'],
                show_id=r['show_id'],
                promo_id=r['promo_id'],
                total_price=r['total_price'],
                service_fee=r['service_fee'],
                status=r['status'],
                booking_date=r['booking_date'],
                created_at=r['created_at']
            )
        return None
