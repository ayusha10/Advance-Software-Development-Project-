
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('Admin', 'Manager', 'Booking-Staff')),
    assigned_cinema_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, password, role) VALUES
('admin26', 'admin@2026', 'Admin'),
('manager26', 'manager@2026', 'Manager'),
('staff26', 'staff@26', 'Booking-Staff');


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
('HORIZON CINEMA LONDON', 4);


CREATE TABLE screens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cinema_id INTEGER NOT NULL,
    screen_number INTEGER NOT NULL,
    total_seats INTEGER NOT NULL,
    FOREIGN KEY (cinema_id) REFERENCES cinemas(id) ON DELETE CASCADE
);


INSERT INTO screens (cinema_id, screen_number, total_seats) VALUES 
(1, 1, 60),
(2, 1, 50),
(3, 2, 20),
(4, 3, 70);


CREATE TABLE films (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    genre TEXT,
    age_rating INTEGER,
    description TEXT,
    time_duration INTEGER NOT NULL
);


INSERT INTO films (name, genre, age_rating, description, time_duration) VALUES
('Maverick', 'Action', 18, 'Drama', 130),
('Spider-Man', 'Action Drama', 16, 'No Way Home', 148),
('Avatar 2', 'Sci-Fi', 12, 'Epic science fiction film', 180),
('The Batman', 'Action', 15, 'Superhero action film', 165),
('Frozen 3', 'Animation', 0, 'Family animation movie', 120);


CREATE TABLE shows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    film_id INTEGER NOT NULL,
    screen_id INTEGER NOT NULL,
    show_date TEXT NOT NULL,
    show_time TEXT NOT NULL,
    base_price REAL NOT NULL,
    FOREIGN KEY (film_id) REFERENCES films(id) ON DELETE CASCADE,
    FOREIGN KEY (screen_id) REFERENCES screen(id) ON DELETE CASCADE,
    UNIQUE(screen_id, show_date, show_time)
);


INSERT INTO shows (film_id, screen_id, show_date, show_time, base_price) VALUES 
(1, 1, '2026-03-01', '10:00:00', 5.00), 
(2, 2, '2026-03-02', '14:00:00', 6.00),
(3, 3, '2026-03-03', '18:00:00', 7.00),
(4, 3, '2026-03-04', '19:00:00', 7.50);


CREATE TABLE seats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    screen_id INTEGER NOT NULL,
    seat_number TEXT NOT NULL,
    seat_type TEXT NOT NULL CHECK(seat_type IN ('Lower', 'Upper', 'VIP')),
    FOREIGN KEY (screen_id) REFERENCES screen(id) ON DELETE CASCADE,
    UNIQUE(screen_id, seat_number)
);


INSERT INTO seats (screen_id, seat_number, seat_type) VALUES
(1, 'A1', 'Lower'),
(1, 'A2', 'Lower'),
(1, 'A3', 'Upper'),
(1, 'A4', 'VIP');


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