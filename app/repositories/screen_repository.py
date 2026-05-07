from config.database import get_connection
import app.models.screen

class ScreenRepository:
    def get_all_screens(self, cinema_id=None):
        connection = get_connection()
        connection.row_factory = __import__('sqlite3').Row
        cursor = connection.cursor()
        if cinema_id:
            query = """
                SELECT s.*, c.name as cinema_name 
                FROM screens s
                JOIN cinemas c ON s.cinema_id = c.id
                WHERE s.cinema_id = ?
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
            result = dict(result)
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
        query = "INSERT INTO screens (cinema_id, screen_number, total_seats) VALUES (?, ?, ?)"
        cursor.execute(query, (screen.cinema_id, screen.screen_number, screen.total_seats))
        connection.commit()
        screen_id = cursor.lastrowid
        
        # Automatically generate seats for this screen
        lower_count = int(round(screen.total_seats * 0.3))
        upper_total = max(0, screen.total_seats - lower_count)
        vip_count = min(10, upper_total)
        upper_count = max(0, upper_total - vip_count)

        seat_index = 1
        for _ in range(lower_count):
            cursor.execute("INSERT INTO seats (screen_id, seat_number, seat_type) VALUES (?, ?, ?)",
                           (screen_id, f"A{seat_index}", "Lower"))
            seat_index += 1

        for _ in range(upper_count):
            cursor.execute("INSERT INTO seats (screen_id, seat_number, seat_type) VALUES (?, ?, ?)",
                           (screen_id, f"B{seat_index}", "Upper"))
            seat_index += 1

        for _ in range(vip_count):
            cursor.execute("INSERT INTO seats (screen_id, seat_number, seat_type) VALUES (?, ?, ?)",
                           (screen_id, f"VIP{seat_index}", "VIP"))
            seat_index += 1
        
        connection.commit()
        cursor.close()
        connection.close()
        return screen_id

    def update_screen(self, screen):
        connection = get_connection()
        cursor = connection.cursor()
        query = "UPDATE screens SET cinema_id = ?, screen_number = ?, total_seats = ? WHERE id = ?"
        cursor.execute(query, (screen.cinema_id, screen.screen_number, screen.total_seats, screen.id))
        connection.commit()
        cursor.close()
        connection.close()

    def delete_screen(self, screen_id):
        connection = get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM screens WHERE id = ?"
        cursor.execute(query, (screen_id,))
        connection.commit()
        cursor.close()
        connection.close()
