from config.database import get_connection
from app.models.film import Film

class FilmRepository:
    def get_all_films(self):
        connection = get_connection()
        connection.row_factory = __import__('sqlite3').Row
        cursor = connection.cursor()
        query = "SELECT id, name, genre, age_rating, description, time_duration FROM films"
        cursor.execute(query)
        results = cursor.fetchall()

        films = []
        for result in results:
            result = dict(result)
            films.append(Film(
                id=result['id'],
                name=result['name'],
                genre=result['genre'],
                age_rating=result['age_rating'],
                description=result['description'],
                time_duration=result['time_duration']
            ))
        cursor.close()
        connection.close()
        return films

    def add_film(self, film):
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO films (name, genre, age_rating, description, time_duration) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (film.name, film.genre, film.age_rating, film.description, film.time_duration))
        connection.commit()
        film_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return film_id

    def delete_film(self, film_id):
        connection = get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM films WHERE id = ?"
        cursor.execute(query, (film_id,))
        connection.commit()
        cursor.close()
        connection.close()
