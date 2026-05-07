from config.database import get_connection
from app.models.show import Show

class ShowRepository:
    def get_all_shows(self, cinema_id=None):
        connection = get_connection()
        connection.row_factory = __import__('sqlite3').Row
        cursor = connection.cursor()
        query = """
            SELECT s.*, f.name as film_name, c.name as cinema_name, ci.name as city_name, sc.screen_number, sc.total_seats,
            (SELECT COUNT(*) FROM booked_seats bs 
             JOIN bookings b ON bs.booking_id = b.id 
             WHERE bs.show_id = s.id AND b.status != 'CANCELLED') as booked_count,
            (SELECT COUNT(*) FROM seats st WHERE st.screen_id = s.screen_id AND st.seat_type = 'Lower') as lower_total,
            (SELECT COUNT(*) FROM seats st WHERE st.screen_id = s.screen_id AND st.seat_type = 'Upper') as upper_total,
            (SELECT COUNT(*) FROM seats st WHERE st.screen_id = s.screen_id AND st.seat_type = 'VIP') as vip_total,
            (SELECT COUNT(*) FROM booked_seats bs JOIN bookings b ON bs.booking_id = b.id JOIN seats st ON bs.seat_id = st.id WHERE bs.show_id = s.id AND b.status != 'CANCELLED' AND st.seat_type = 'Lower') as lower_booked,
            (SELECT COUNT(*) FROM booked_seats bs JOIN bookings b ON bs.booking_id = b.id JOIN seats st ON bs.seat_id = st.id WHERE bs.show_id = s.id AND b.status != 'CANCELLED' AND st.seat_type = 'Upper') as upper_booked,
            (SELECT COUNT(*) FROM booked_seats bs JOIN bookings b ON bs.booking_id = b.id JOIN seats st ON bs.seat_id = st.id WHERE bs.show_id = s.id AND b.status != 'CANCELLED' AND st.seat_type = 'VIP') as vip_booked
            FROM shows s
            JOIN films f ON s.film_id = f.id
            JOIN screens sc ON s.screen_id = sc.id
            JOIN cinemas c ON sc.cinema_id = c.id
            JOIN cities ci ON c.city_id = ci.id
        """
        params = []
        if cinema_id:
            query += " WHERE c.id = ?"
            params.append(cinema_id)
        cursor.execute(query, params)
        results = cursor.fetchall()

        shows = []
        for r in results:
            r = dict(r)
            available = r['total_seats'] - r['booked_count']
            lower_av = r['lower_total'] - r['lower_booked']
            upper_av = r['upper_total'] - r['upper_booked']
            vip_av = r['vip_total'] - r['vip_booked']
            shows.append(Show(
                id=r['id'],
                film_id=r['film_id'],
                screen_id=r['screen_id'],
                show_date=r['show_date'],
                show_time=r['show_time'],
                base_price=r['base_price'],
                film_name=r['film_name'],
                cinema_name=r['cinema_name'],
                city_name=r['city_name'],
                screen_number=r['screen_number'],
                available_seats=available,
                lower_available=lower_av,
                upper_available=upper_av,
                vip_available=vip_av
            ))
        cursor.close()
        connection.close()
        return shows

    def add_show(self, show):
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO shows (film_id, screen_id, show_date, show_time, base_price) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (show.film_id, show.screen_id, show.show_date, show.show_time, show.base_price))
        connection.commit()
        show_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return show_id

    def delete_show(self, show_id):
        connection = get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM shows WHERE id = ?"
        cursor.execute(query, (show_id,))
        connection.commit()
        cursor.close()
        connection.close()

    def update_show(self, show):
        connection = get_connection()
        cursor = connection.cursor()
        query = "UPDATE shows SET film_id = ?, screen_id = ?, show_date = ?, show_time = ?, base_price = ? WHERE id = ?"
        cursor.execute(query, (show.film_id, show.screen_id, show.show_date, show.show_time, show.base_price, show.id))
        connection.commit()
        cursor.close()
        connection.close()

    def get_show_by_id(self, show_id):
        connection = get_connection()
        connection.row_factory = __import__('sqlite3').Row
        cursor = connection.cursor()
        query = """
            SELECT s.*, f.name as film_name, c.name as cinema_name, ci.name as city_name, sc.screen_number, sc.total_seats,
            (SELECT COUNT(*) FROM booked_seats bs 
             JOIN bookings b ON bs.booking_id = b.id 
             WHERE bs.show_id = s.id AND b.status != 'CANCELLED') as booked_count,
            (SELECT COUNT(*) FROM seats st WHERE st.screen_id = s.screen_id AND st.seat_type = 'Lower') as lower_total,
            (SELECT COUNT(*) FROM seats st WHERE st.screen_id = s.screen_id AND st.seat_type = 'Upper') as upper_total,
            (SELECT COUNT(*) FROM seats st WHERE st.screen_id = s.screen_id AND st.seat_type = 'VIP') as vip_total,
            (SELECT COUNT(*) FROM booked_seats bs JOIN bookings b ON bs.booking_id = b.id JOIN seats st ON bs.seat_id = st.id WHERE bs.show_id = s.id AND b.status != 'CANCELLED' AND st.seat_type = 'Lower') as lower_booked,
            (SELECT COUNT(*) FROM booked_seats bs JOIN bookings b ON bs.booking_id = b.id JOIN seats st ON bs.seat_id = st.id WHERE bs.show_id = s.id AND b.status != 'CANCELLED' AND st.seat_type = 'Upper') as upper_booked,
            (SELECT COUNT(*) FROM booked_seats bs JOIN bookings b ON bs.booking_id = b.id JOIN seats st ON bs.seat_id = st.id WHERE bs.show_id = s.id AND b.status != 'CANCELLED' AND st.seat_type = 'VIP') as vip_booked
            FROM shows s
            JOIN films f ON s.film_id = f.id
            JOIN screens sc ON s.screen_id = sc.id
            JOIN cinemas c ON sc.cinema_id = c.id
            JOIN cities ci ON c.city_id = ci.id
            WHERE s.id = ?
        """
        cursor.execute(query, (show_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if result:
            r = dict(result)
            available = r['total_seats'] - r['booked_count']
            lower_av = r['lower_total'] - r['lower_booked']
            upper_av = r['upper_total'] - r['upper_booked']
            vip_av = r['vip_total'] - r['vip_booked']
            return Show(
                id=r['id'],
                film_id=r['film_id'],
                screen_id=r['screen_id'],
                show_date=r['show_date'],
                show_time=r['show_time'],
                base_price=r['base_price'],
                film_name=r['film_name'],
                cinema_name=r['cinema_name'],
                city_name=r['city_name'],
                screen_number=r['screen_number'],
                available_seats=available,
                lower_available=lower_av,
                upper_available=upper_av,
                vip_available=vip_av
            )
        return None
