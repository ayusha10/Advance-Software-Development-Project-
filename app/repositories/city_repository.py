from config.database import get_connection
from app.models.city import City

class CityRepository:
    def get_all_cities(self):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM cities"
        cursor.execute(query)
        results = cursor.fetchall()
        
        cities = []
        for result in results:
            cities.append(City(
                id=result['id'],
                name=result['name']
            ))
        
        cursor.close()
        connection.close()
        return cities

    def add_city(self, city_name):
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO cities (name) VALUES (%s)"
        cursor.execute(query, (city_name,))
        connection.commit()
        city_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return city_id

    def delete_city(self, city_id):
        connection = get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM cities WHERE id = %s"
        cursor.execute(query, (city_id,))
        connection.commit()
        cursor.close()
        connection.close()
