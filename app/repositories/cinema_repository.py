from config.database import get_connection
from app.models.cinema import Cinema

class CinemaRepository:
    def get_all_cinemas(self):
        connection = get_connection()
        connection.row_factory = __import__('sqlite3').Row
        cursor = connection.cursor()
        query = """
            SELECT c.*, ci.name as city_name 
            FROM cinemas c
            JOIN cities ci ON c.city_id = ci.id
        """
        cursor.execute(query)
        results = cursor.fetchall()

        cinemas = []
        for result in results:
            result = dict(result)
            cinemas.append(Cinema(
                id=result['id'],
                name=result['name'],
                city_id=result['city_id'],
                city_name=result['city_name']
            ))
        cursor.close()
        connection.close()
        return cinemas

    def add_cinema(self, cinema):
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO cinemas (name, city_id) VALUES (?, ?)"
        cursor.execute(query, (cinema.name, cinema.city_id))
        connection.commit()
        cinema_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return cinema_id

    def update_cinema(self, cinema):
        connection = get_connection()
        cursor = connection.cursor()
        query = "UPDATE cinemas SET name = ?, city_id = ? WHERE id = ?"
        cursor.execute(query, (cinema.name, cinema.city_id, cinema.id))
        connection.commit()
        cursor.close()
        connection.close()

    def delete_cinema(self, cinema_id):
        connection = get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM cinemas WHERE id = ?"
        cursor.execute(query, (cinema_id,))
        connection.commit()
        cursor.close()
        connection.close()
