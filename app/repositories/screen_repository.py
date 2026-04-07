from config.database import get_connection
import app.models.screen

class ScreenRepository:
    def get_all_screens(self, cinema_id=None):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        if cinema_id:
            query = """
                SELECT s.*, c.name as cinema_name 
                FROM screens s
                JOIN cinemas c ON s.cinema_id = c.id
                WHERE s.cinema_id = %s
            """
            cursor.execute(query, (cinema_id,))
        else:
            query = """
                SELECT s.*, c.name as cinema_name 
                FROM screens s
                JOIN cinemas c ON s.cinema_id = c.id
            """
            cursor.execute(query)
        results = cursor.fetchall()
        
        screens = []
        for result in results:
            screens.append(app.models.screen.Screen(
                id=result['id'],
                cinema_id=result['cinema_id'],
                screen_number=result['screen_number'],
                total_seats=result['total_seats'],
                cinema_name=result['cinema_name']
            ))
        
        cursor.close()
        connection.close()
        return screens

    def add_screen(self, screen):
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO screens (cinema_id, screen_number, total_seats) VALUES (%s, %s, %s)"
        cursor.execute(query, (screen.cinema_id, screen.screen_number, screen.total_seats))
        connection.commit()
        screen_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return screen_id

    def update_screen(self, screen):
        connection = get_connection()
        cursor = connection.cursor()
        query = "UPDATE screens SET cinema_id = %s, screen_number = %s, total_seats = %s WHERE id = %s"
        cursor.execute(query, (screen.cinema_id, screen.screen_number, screen.total_seats, screen.id))
        connection.commit()
        cursor.close()
        connection.close()

    def delete_screen(self, screen_id):
        connection = get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM screens WHERE id = %s"
        cursor.execute(query, (screen_id,))
        connection.commit()
        cursor.close()
        connection.close()
