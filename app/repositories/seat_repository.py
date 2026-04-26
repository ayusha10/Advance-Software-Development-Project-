from config.database import get_connection
import app.models.seat

class SeatRepository:
    def get_all_seats(self):
        connection = get_connection()
        connection.row_factory = __import__('sqlite3').Row
        cursor = connection.cursor()
        query = """
            SELECT s.*, c.name || ' - Screen ' || sc.screen_number as screen_info
            FROM seats s
            JOIN screens sc ON s.screen_id = sc.id
            JOIN cinemas c ON sc.cinema_id = c.id
        """
        cursor.execute(query)
        results = cursor.fetchall()

        seats = []
        for result in results:
            result = dict(result)
            seats.append(app.models.seat.Seat(
                id=result['id'],
                screen_id=result['screen_id'],
                seat_number=result['seat_number'],
                seat_type=result['seat_type'],
                screen_info=result['screen_info']
            ))
        cursor.close()
        connection.close()
        return seats

    def add_seat(self, seat):
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO seats (screen_id, seat_number, seat_type) VALUES (?, ?, ?)"
        cursor.execute(query, (seat.screen_id, seat.seat_number, seat.seat_type))
        connection.commit()
        seat_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return seat_id

    def update_seat(self, seat):
        connection = get_connection()
        cursor = connection.cursor()
        query = "UPDATE seats SET screen_id = ?, seat_number = ?, seat_type = ? WHERE id = ?"
        cursor.execute(query, (seat.screen_id, seat.seat_number, seat.seat_type, seat.id))
        connection.commit()
        cursor.close()
        connection.close()

    def delete_seat(self, seat_id):
        connection = get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM seats WHERE id = ?"
        cursor.execute(query, (seat_id,))
        connection.commit()
        cursor.close()
        connection.close()
