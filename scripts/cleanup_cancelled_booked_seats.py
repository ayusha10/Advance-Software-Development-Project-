import sqlite3


def main():
    conn = sqlite3.connect("horizon_db.sqlite3")
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM booked_seats WHERE booking_id IN (SELECT id FROM bookings WHERE status = 'CANCELLED')"
    )
    deleted = cur.rowcount
    conn.commit()
    conn.close()
    print(f"deleted_rows={deleted}")


if __name__ == "__main__":
    main()
