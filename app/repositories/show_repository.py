from config.database import get_connection
from app.models.show import Show

class ShowRepository:
    def get_all_shows(self, cinema_id=None):
        connection = get_connection()
        connection.row_factory = __import__('sqlite3').Row
        cursor = connection.cursor()
        query = """
            SELECT s.*, f.name as film_name, c.name as cinema_name, sc.screen_number 
            FROM shows s
            JOIN films f ON s.film_id = f.id
            JOIN screens sc ON s.screen_id = sc.id
            JOIN cinemas c ON sc.cinema_id = c.id
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
            shows.append(Show(
                id=r['id'],
                film_id=r['film_id'],
                screen_id=r['screen_id'],
                show_time=r['show_time'],
                base_price=r['base_price'],
                film_name=r['film_name'],
                cinema_name=r['cinema_name'],
                screen_number=r['screen_number']
            ))
        cursor.close()
        connection.close()
        return shows

    def add_show(self, show):
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO shows (film_id, screen_id, show_time, base_price) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (show.film_id, show.screen_id, show.show_time, show.base_price))
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
