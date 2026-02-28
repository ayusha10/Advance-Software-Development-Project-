DROP DATABASE IF EXISTS horizon_db;
CREATE DATABASE horizon_db;
USE horizon_db;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'Manager', 'Booking-Staff') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, password, role) VALUES
('admin26', 'admin@2026', 'Admin'),
('manager26', 'manager@2026', 'Manager'),
('staff26', 'staff@26', 'Booking-Staff');

#create city table 
CREATE TABLE cities (
	id INT PRIMARY KEY AUTO_INCREMENT, 
    name VARCHAR (100) UNIQUE NOT NULL
);

#insert values 
INSERT INTO cities ( name ) VALUES 
('Birmingham'),
('Bristol'),
('Cardiff'),
('London');

CREATE TABLE cinema (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    city_id INT NOT NULL,
    FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
);

#insert values 
INSERT INTO cinema (name, city_id) VALUES 
('HORIZON CINEMA BIRMINGHAM', 1), 
('HORIZON CINEMA BRISTOL', 2),
('HORIZON CINEMA CARDIFF', 3),
('HORIZON CINEMA LONDON', 4);

CREATE TABLE screen (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cinema_id INT NOT NULL,
    screen_number INT NOT NULL,
    total_seats INT NOT NULL,
    FOREIGN KEY (cinema_id) REFERENCES cinema(id) ON DELETE CASCADE
);

#insert values 
INSERT INTO screen (cinema_id, screen_number, total_seats) VALUES 
(1, 1, 60),
(2, 1, 50),
(3, 2,20),
(4, 3,70);

CREATE TABLE films (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    genre VARCHAR(50),
    age_rating INT,
    description TEXT,
    time_duration INT NOT NULL
);

#insert values of flim 
INSERT INTO films (name, genre, age_rating,  description, time_duration) VALUES
('Maverick', 'Action', 18,'Drama', 130),
('Spider-Man', 'Action Drama', 16, 'No Way Home', 148),
('Avatar 2','Sci-Fi',12,'Epic science fiction film',180),
('The Batman','Action',15,'Superhero action film',165),
('Frozen 3','Animation',0,'Family animation movie',120);

CREATE TABLE shows (
    id INT PRIMARY KEY AUTO_INCREMENT,
    film_id INT NOT NULL,
    screen_id INT NOT NULL,
    show_date DATE NOT NULL,
    show_time TIME NOT NULL,
    base_price DECIMAL(10,2) NOT NULL,
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
    id INT PRIMARY KEY AUTO_INCREMENT,
    screen_id INT NOT NULL,
    seat_number VARCHAR(10) NOT NULL,
    seat_type ENUM('Lower', 'Upper', 'VIP') NOT NULL,
    FOREIGN KEY (screen_id) REFERENCES screen(id) ON DELETE CASCADE,
    UNIQUE(screen_id, seat_number)
);

#insert Seats value 
INSERT INTO seats (screen_id, seat_number, seat_type) VALUES
(1, 'A1', 'Lower'),
(1, 'A2', 'Lower'),
(1, 'A3', 'Upper'),
(1, 'A4', 'VIP');

CREATE TABLE promotions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    promo_code VARCHAR(50) UNIQUE NOT NULL,
    discount_percentage DECIMAL(5,2) NOT NULL,
    valid_from DATE NOT NULL,
    valid_to DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_promo_code ON promotions(promo_code);
CREATE INDEX idx_promo_active ON promotions(is_active);
CREATE INDEX idx_promo_validity ON promotions(valid_from, valid_to);


CREATE TABLE bookings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    booking_ref VARCHAR(20) UNIQUE NOT NULL,
    user_id INT NOT NULL,
    show_id INT NOT NULL,
    promo_id INT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    service_fee DECIMAL(10,2) DEFAULT 5.00,
    status ENUM('CONFIRMED', 'CANCELLED') DEFAULT 'CONFIRMED',
    booking_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (show_id) REFERENCES shows(id) ON DELETE CASCADE,
    FOREIGN KEY (promo_id) REFERENCES promotions(id) ON DELETE SET NULL
);


CREATE INDEX idx_booking_show ON bookings(show_id);
CREATE INDEX idx_booking_date ON bookings(booking_date);
CREATE INDEX idx_booking_created_at ON bookings(created_at);

CREATE TABLE booked_seats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT NOT NULL,
    show_id INT NOT NULL,
    seat_id INT NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
    FOREIGN KEY (show_id) REFERENCES shows(id) ON DELETE CASCADE,
    FOREIGN KEY (seat_id) REFERENCES seats(id) ON DELETE CASCADE,
    UNIQUE(seat_id, show_id)
);

CREATE INDEX idx_booked_seats_booking ON booked_seats(booking_id);
CREATE INDEX idx_booked_seats_show ON booked_seats(show_id);
CREATE INDEX idx_booked_seats_seat ON booked_seats(seat_id);

CREATE TABLE payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT NOT NULL,
    amount_paid DECIMAL(10,2) NOT NULL,
    payment_method ENUM('Cash', 'Card', 'Online') NOT NULL,
    payment_status ENUM('PAID', 'FAILED', 'REFUNDED') DEFAULT 'PAID',
    transaction_reference VARCHAR(100),
    paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
);
CREATE INDEX idx_payment_booking ON payments(booking_id);
CREATE INDEX idx_payment_status ON payments(payment_status);
CREATE INDEX idx_payment_method ON payments(payment_method);
CREATE INDEX idx_payment_date ON payments(paid_at);

CREATE TABLE cancellations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT NOT NULL,
    reason TEXT,
    refund_amount DECIMAL(10,2),
    cancelled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
);

CREATE INDEX idx_cancel_booking ON cancellations(booking_id);
CREATE INDEX idx_cancel_date ON cancellations(cancelled_at);

CREATE TABLE seat_locks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    show_id INT NOT NULL,
    seat_id INT NOT NULL,
    locked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (show_id) REFERENCES shows(id) ON DELETE CASCADE,
    FOREIGN KEY (seat_id) REFERENCES seats(id) ON DELETE CASCADE,
    UNIQUE(seat_id, show_id)
);
CREATE INDEX idx_lock_show ON seat_locks(show_id);
CREATE INDEX idx_lock_seat ON seat_locks(seat_id);
CREATE INDEX idx_lock_time ON seat_locks(locked_at);

CREATE TABLE system_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action TEXT,
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
    
);

CREATE INDEX idx_log_user ON system_logs(user_id);
CREATE INDEX idx_log_time ON system_logs(action_time);

CREATE INDEX idx_show_date ON shows(show_date);
CREATE INDEX idx_film_id ON shows(film_id);
CREATE INDEX idx_user_id ON bookings(user_id);
CREATE INDEX idx_booking_status ON bookings(status);