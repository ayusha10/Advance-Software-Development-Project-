
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('Admin', 'Manager', 'Booking-Staff', 'Customer')),
    assigned_city_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, password, role, assigned_city_id) VALUES
('admin26', 'admin1234', 'Admin', NULL),
('manager26', 'manager@2026', 'Manager', 3),
('customer26', 'customer26', 'Customer', NULL),

('Ayusha', 'ayusha1234', 'Customer', NULL),

('staff1', 'staff@2026', 'Booking-Staff', 1),
('customer1', 'cust@2026', 'Customer', NULL),
('staff26', 'staff@26', 'Booking-Staff', 1),
('pras', 'pras', 'Customer', NULL);


CREATE TABLE cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);


INSERT INTO cities (name) VALUES 
('Birmingham'),
('Bristol'),
('Cardiff'),
('London');


CREATE TABLE cinemas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    city_id INTEGER NOT NULL,
    FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
);


INSERT INTO cinemas (name, city_id) VALUES 
('HORIZON CINEMA BIRMINGHAM', 1), 
('HORIZON CINEMA BRISTOL', 2),
('HORIZON CINEMA CARDIFF', 3),
('HORIZON CINEMA LONDON', 4),
('Horizon Cinema Birmingham Star City', 1),
('Horizon Cinema Bristol Cribbs Causeway', 2),
('Horizon Cinema Cardiff Gate', 3),
('Horizon Cinema London Canary Wharf', 4);


CREATE TABLE screens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cinema_id INTEGER NOT NULL,
    screen_number INTEGER NOT NULL,
    total_seats INTEGER NOT NULL,
    FOREIGN KEY (cinema_id) REFERENCES cinemas(id) ON DELETE CASCADE
);


INSERT INTO screens (cinema_id, screen_number, total_seats) VALUES 
(1, 1, 70),
(2, 1, 70),
(3, 2, 70),
(4, 3, 70),
(1, 2, 70),
(2, 2, 70),
(3, 2, 70),
(4, 2, 70),
(5, 2, 70),
(6, 2, 70),
(7, 2, 70),
(8, 2, 70);


CREATE TABLE films (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    genre TEXT,
    age_rating INTEGER,
    description TEXT,
    actors TEXT,
    time_duration INTEGER NOT NULL
);


INSERT INTO films (name, genre, age_rating, description, actors, time_duration) VALUES
('Maverick', 'Action', 18, 'Drama', 'Tom Cruise, Miles Teller, Jennifer Connelly', 130),
('Spider-Man', 'Action Drama', 16, 'No Way Home', 'Tom Holland, Zendaya, Benedict Cumberbatch', 148),
('Avatar 2', 'Sci-Fi', 12, 'Epic science fiction film', 'Sam Worthington, Zoe Saldana, Sigourney Weaver', 180),
('The Batman', 'Action', 15, 'Superhero action film', 'Robert Pattinson, Zoë Kravitz, Paul Dano', 165),
('Frozen 3', 'Animation', 0, 'Family animation movie', 'Idina Menzel, Kristen Bell, Josh Gad', 120);


CREATE TABLE shows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    film_id INTEGER NOT NULL,
    screen_id INTEGER NOT NULL,
    show_date TEXT NOT NULL,
    show_time TEXT NOT NULL,
    base_price REAL NOT NULL,
    FOREIGN KEY (film_id) REFERENCES films(id) ON DELETE CASCADE,
    FOREIGN KEY (screen_id) REFERENCES screens(id) ON DELETE CASCADE,
    UNIQUE(screen_id, show_date, show_time)
);


INSERT INTO shows (film_id, screen_id, show_date, show_time, base_price) VALUES 
(1, 1, '2026-05-13', '10:00:00', 5.00),
(2, 2, '2026-05-14', '14:00:00', 6.00),
(3, 3, '2026-05-15', '18:00:00', 7.00),
(4, 3, '2026-05-16', '19:00:00', 7.50),
(1, 1, '2026-05-06', '18:00:00', 10.00),
(4, 4, '2026-05-13', '10:00:00', 5.00),
(5, 6, '2026-05-13', '14:00:00', 6.00),
(1, 7, '2026-05-13', '18:00:00', 7.00),
(2, 8, '2026-05-13', '10:00:00', 5.00),
(3, 9, '2026-05-13', '14:00:00', 6.00),
(4, 10, '2026-05-13', '18:00:00', 7.00),
(5, 11, '2026-05-13', '10:00:00', 5.00),
(1, 12, '2026-05-13', '14:00:00', 6.00),
(2, 13, '2026-05-13', '18:00:00', 7.00);


CREATE TABLE seats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    screen_id INTEGER NOT NULL,
    seat_number TEXT NOT NULL,
    seat_type TEXT NOT NULL CHECK(seat_type IN ('Lower', 'Upper', 'VIP')),
    FOREIGN KEY (screen_id) REFERENCES screens(id) ON DELETE CASCADE,
    UNIQUE(screen_id, seat_number)
);


INSERT OR IGNORE INTO seats (screen_id, seat_number, seat_type)
WITH RECURSIVE nums(n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM nums WHERE n < 70
)
SELECT
    s.id,
    CASE
        WHEN nums.n <= 21 THEN printf('L%02d', nums.n)
        WHEN nums.n <= 60 THEN printf('U%02d', nums.n - 21)
        ELSE printf('VIP%02d', nums.n - 60)
    END,
    CASE
        WHEN nums.n <= 21 THEN 'Lower'
        WHEN nums.n <= 60 THEN 'Upper'
        ELSE 'VIP'
    END
FROM screens s
CROSS JOIN nums;


CREATE TABLE promotions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    promo_code TEXT UNIQUE NOT NULL,
    discount_percentage REAL NOT NULL,
    valid_from TEXT NOT NULL,
    valid_to TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_promo_code ON promotions(promo_code);
CREATE INDEX idx_promo_active ON promotions(is_active);
CREATE INDEX idx_promo_validity ON promotions(valid_from, valid_to);



CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_ref TEXT UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    show_id INTEGER NOT NULL,
    promo_id INTEGER,
    total_price REAL NOT NULL,
    service_fee REAL DEFAULT 5.00,
    status TEXT DEFAULT 'CONFIRMED' CHECK(status IN ('CONFIRMED', 'CANCELLED')),
    booking_date TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (show_id) REFERENCES shows(id) ON DELETE CASCADE,
    FOREIGN KEY (promo_id) REFERENCES promotions(id) ON DELETE SET NULL
);



CREATE INDEX idx_booking_show ON bookings(show_id);
CREATE INDEX idx_booking_date ON bookings(booking_date);
CREATE INDEX idx_booking_created_at ON bookings(created_at);


CREATE TABLE booked_seats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER NOT NULL,
    show_id INTEGER NOT NULL,
    seat_id INTEGER NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
    FOREIGN KEY (show_id) REFERENCES shows(id) ON DELETE CASCADE,
    FOREIGN KEY (seat_id) REFERENCES seats(id) ON DELETE CASCADE,
    UNIQUE(seat_id, show_id)
);


CREATE INDEX idx_booked_seats_booking ON booked_seats(booking_id);
CREATE INDEX idx_booked_seats_show ON booked_seats(show_id);
CREATE INDEX idx_booked_seats_seat ON booked_seats(seat_id);


CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER NOT NULL,
    amount_paid REAL NOT NULL,
    payment_method TEXT NOT NULL CHECK(payment_method IN ('Cash', 'Card', 'Online')),
    payment_status TEXT DEFAULT 'PAID' CHECK(payment_status IN ('PAID', 'FAILED', 'REFUNDED')),
    transaction_reference TEXT,
    paid_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
);
CREATE INDEX idx_payment_booking ON payments(booking_id);
CREATE INDEX idx_payment_status ON payments(payment_status);
CREATE INDEX idx_payment_method ON payments(payment_method);
CREATE INDEX idx_payment_date ON payments(paid_at);


CREATE TABLE cancellations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER NOT NULL,
    reason TEXT,
    refund_amount REAL,
    cancelled_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
);


CREATE INDEX idx_cancel_booking ON cancellations(booking_id);
CREATE INDEX idx_cancel_date ON cancellations(cancelled_at);


CREATE TABLE seat_locks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    show_id INTEGER NOT NULL,
    seat_id INTEGER NOT NULL,
    locked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (show_id) REFERENCES shows(id) ON DELETE CASCADE,
    FOREIGN KEY (seat_id) REFERENCES seats(id) ON DELETE CASCADE,
    UNIQUE(seat_id, show_id)
);
CREATE INDEX idx_lock_show ON seat_locks(show_id);
CREATE INDEX idx_lock_seat ON seat_locks(seat_id);
CREATE INDEX idx_lock_time ON seat_locks(locked_at);


CREATE TABLE system_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,
    action_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);
CREATE INDEX idx_log_user ON system_logs(user_id);
CREATE INDEX idx_log_time ON system_logs(action_time);


CREATE INDEX idx_show_date ON shows(show_date);
CREATE INDEX idx_film_id ON shows(film_id);
CREATE INDEX idx_user_id ON bookings(user_id);
CREATE INDEX idx_booking_status ON bookings(status);