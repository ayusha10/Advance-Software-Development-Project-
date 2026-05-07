from config.database import get_connection
from app.models.film import Film

class FilmRepository:
    def _get_film_columns(self, connection):
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info(films)")
        columns = {row[1] for row in cursor.fetchall()}
        cursor.close()
        return columns

    def get_all_films(self):
        connection = get_connection()
        connection.row_factory = __import__('sqlite3').Row
        cursor = connection.cursor()
        columns = self._get_film_columns(connection)
        select_columns = ["id", "name", "genre", "age_rating", "description", "time_duration"]
        if "actors" in columns:
            select_columns.append("actors")
        query = f"SELECT {', '.join(select_columns)} FROM films"
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
                time_duration=result['time_duration'],
                actors=result.get('actors')
            ))
        cursor.close()
        connection.close()
        return films

    def add_film(self, film):
        connection = get_connection()
        cursor = connection.cursor()
        columns = self._get_film_columns(connection)
        if "actors" in columns:
            query = "INSERT INTO films (name, genre, age_rating, description, time_duration, actors) VALUES (?, ?, ?, ?, ?, ?)"
            cursor.execute(query, (film.name, film.genre, film.age_rating, film.description, film.time_duration, film.actors))
        else:
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

    def update_film(self, film):
        connection = get_connection()
        cursor = connection.cursor()
        columns = self._get_film_columns(connection)
        if "actors" in columns:
            query = "UPDATE films SET name = ?, genre = ?, age_rating = ?, description = ?, time_duration = ?, actors = ? WHERE id = ?"
            cursor.execute(query, (film.name, film.genre, film.age_rating, film.description, film.time_duration, film.actors, film.id))
        else:
            query = "UPDATE films SET name = ?, genre = ?, age_rating = ?, description = ?, time_duration = ? WHERE id = ?"
            cursor.execute(query, (film.name, film.genre, film.age_rating, film.description, film.time_duration, film.id))
        connection.commit()
        cursor.close()
        connection.close()

