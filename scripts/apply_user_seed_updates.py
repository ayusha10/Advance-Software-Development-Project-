import sqlite3


def main():
    conn = sqlite3.connect("horizon_db.sqlite3")
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET password = ? WHERE username = ?",
        ("Admin@2026!", "admin26"),
    )
    cur.execute(
        "UPDATE users SET password = ? WHERE username = ?",
        ("manager@2026", "manager26"),
    )

    cur.execute(
        "INSERT OR IGNORE INTO users (username, password, role, assigned_city_id) VALUES (?, ?, ?, ?)",
        ("staff1", "staff@2026", "Booking-Staff", 1),
    )

    # Keep legacy sample staff account available for login demos.
    cur.execute(
        "INSERT OR IGNORE INTO users (username, password, role, assigned_city_id) VALUES (?, ?, ?, ?)",
        ("staff26", "staff@26", "Booking-Staff", 1),
    )

    cur.execute(
        "INSERT OR IGNORE INTO users (username, password, role, assigned_city_id) VALUES (?, ?, ?, ?)",
        ("customer1", "cust@2026", "Customer", None),
    )

    # Ensure operational city mapping exists for role-based panels.
    cur.execute("UPDATE users SET assigned_city_id = 3 WHERE username = 'manager26' AND assigned_city_id IS NULL")
    cur.execute("UPDATE users SET password = 'staff@2026' WHERE username = 'staff1'")
    cur.execute("UPDATE users SET password = 'staff@26' WHERE username = 'staff26'")
    cur.execute("UPDATE users SET assigned_city_id = 1 WHERE username = 'staff1' AND assigned_city_id IS NULL")
    cur.execute("UPDATE users SET assigned_city_id = 1 WHERE username = 'staff26' AND assigned_city_id IS NULL")

    conn.commit()

    cur.execute(
        "SELECT username, role, assigned_city_id FROM users WHERE username IN ('admin26', 'manager26', 'staff1', 'staff26', 'customer1') ORDER BY username"
    )
    rows = cur.fetchall()
    print(rows)

    cur.execute("SELECT password FROM users WHERE username = 'admin26'")
    pwd_row = cur.fetchone()
    print("admin_password_updated=", bool(pwd_row and pwd_row[0] == "Admin@2026!"))

    conn.close()


if __name__ == "__main__":
    main()
