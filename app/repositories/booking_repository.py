from config.database import get_connection
import app.models.booking

class BookingRepository:
    def get_all_bookings(self, cinema_id=None):
        connection = get_connection()
        connection.row_factory = __import__('sqlite3').Row
        cursor = connection.cursor()
        if cinema_id:
            query = """
                SELECT b.* 
                FROM bookings b
                JOIN shows s ON b.show_id = s.id
                JOIN screens sc ON s.screen_id = sc.id
                WHERE sc.cinema_id = ?
            """
            cursor.execute(query, (cinema_id,))
        else:
            query = "SELECT * FROM bookings"
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
                created_at=result['created_at']
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
