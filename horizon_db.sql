DROP DATABASE IF EXISTS horizon_db;

CREATE DATABASE horizon_db;
USE horizon_db;

#create table for users 
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT, 
    username VARCHAR (100) UNIQUE NOT NULL,
    password VARCHAR (100) NOT NULL, 
    role ENUM ('Booking-Staff', 'Admin', 'Manager') NOT NULL 
);

#Insert the values for users table 
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

#create cinema table 
CREATE TABLE cinema (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR (100) UNIQUE NOT NULL,
    city_id INT NOT NULL, 
    FOREIGN KEY (city_id) REFERENCES cities (id) 
    ON DELETE CASCADE
);

#insert values 
INSERT INTO cinema (name, city_id) VALUES 
('HORIZON CINEMA BIRMINGHAM', 1), 
('HORIZON CINEMA BRISTOL', 2),
('HORIZON CINEMA CARDIFF', 3),
('HORIZON CINEMA LONDON', 4);

#create screen table 
CREATE TABLE screen (
	id INT PRIMARY KEY AUTO_INCREMENT, 
    cinema_id INT NOT NULL, 
    screen_number INT NOT NULL, 
    total_seats INT NOT NULL, 
    FOREIGN KEY (cinema_id) REFERENCES cinema (id)
    ON DELETE CASCADE 
);

#insert values 
INSERT INTO screen (cinema_id, screen_number, total_seats) VALUES 
(1, 1, 60),
(2, 1, 50),
(3, 2,20),
(4, 3,70);

CREATE TABLE films (
   id INT PRIMARY KEY AUTO_INCREMENT, 
    name VARCHAR (100) UNIQUE NOT NULL, 
    genre VARCHAR (50),
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

#create show_time table
CREATE TABLE shows (  
     id INT PRIMARY KEY AUTO_INCREMENT, 
     film_id INT NOT NULL,   
     screen_id INT NOT NULL, 
     show_date DATE NOT NULL,   
     show_time TIME NOT NULL,  
     base_price DECIMAL (10,2) NOT NULL, 
     FOREIGN KEY (film_id) REFERENCES films (id) 
     ON DELETE CASCADE, 
     FOREIGN KEY (screen_id) REFERENCES screen (id)
     ON DELETE CASCADE
);

INSERT INTO shows (film_id, screen_id, show_date, show_time, base_price) VALUES 
(1, 1, '2026-03-01', '10:00:00', 5.00), 
(2, 2, '2026-03-02', '14:00:00', 6.00),
(3, 3, '2026-03-03', '18:00:00', 7.00),
(4, 3, '2026-03-04', '19:00:00', 7.50); 

#create table seats
 CREATE TABLE seats (
    id INT PRIMARY KEY AUTO_INCREMENT, 
    screen_id INT NOT NULL, 
    seat_number VARCHAR(15) NOT NULL, 
    seat_type ENUM ('Lower', 'Upper', 'VIP') NOT NULL, 
    FOREIGN KEY (screen_id) REFERENCES screen (id)
    ON DELETE CASCADE 
);

#insert Seats value 
INSERT INTO seats (screen_id, seat_number, seat_type) VALUES
(1, 'A1', 'Lower'),
(1, 'A2', 'Lower'),
(1, 'A3', 'Upper'),
(1, 'A4', 'VIP');

#create table booking 
CREATE TABLE bookings (
   id INT PRIMARY KEY AUTO_INCREMENT, 
   booking_ref VARCHAR (20) UNIQUE NOT NULL, 
   user_id INT NOT NULL, 
   show_id INT NOT NULL, 
   total_price DECIMAL (10,2) NOT NULL, 
   booking_date DATE NOT NULL, 
   FOREIGN KEY (user_id) REFERENCES users (id),
   FOREIGN KEY (show_id) REFERENCES shows(id)
);
# adding more featurs 
ALTER TABLE bookings
ADD COLUMN status ENUM ('CONFIRMED', 'CANCELLED') DEFAULT 'CONFIRMED';

ALTER TABLE bookings 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE users 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE bookings 
ADD COLUMN service_fee DECIMAL (10,2) DEFAULT 5.00;

#insert value for booking 
INSERT INTO bookings 
(booking_ref, user_id, show_id, total_price, booking_date) 
VALUES 
('BK001', 3, 1, 20.00, '2026-03-01'),
('BK002', 2, 2, 15.00, '2026-03-02');

#create table booked_seats
CREATE TABLE booked_seats (
    id INT PRIMARY KEY AUTO_INCREMENT, 
    booking_id INT NOT NULL, 
    seat_id INT NOT NULL, 
    FOREIGN KEY (booking_id) REFERENCES bookings (id)
    ON DELETE CASCADE, 
    FOREIGN KEY (seat_id) REFERENCES seats (id) 
    ON DELETE CASCADE
); 

#insert values for booked_seats 
INSERT INTO booked_seats (booking_id, seat_id)
VALUES 
(1, 1),
(1, 2),
(2, 3),
(2, 1);

#create table seat pricing 
CREATE TABLE seat_pricing(
	id INT PRIMARY KEY AUTO_INCREMENT, 
    seat_type ENUM ('Lower', 'Upper', 'VIP') UNIQUE, 
    multiplier DECIMAL(3,2) NOT NULL 
);

INSERT INTO seat_pricing (seat_type, multiplier) VALUES 
('Lower', 1.00),
('Upper', 1.50),
('VIP', 2.00);

#system log table 
CREATE TABLE system_logs(
     id INT PRIMARY KEY AUTO_INCREMENT, 
     user_id INT, 
     action TEXT, 
     action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
     FOREIGN KEY (user_id) REFERENCES users(id)
);

#create payment system 
CREATE TABLE payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT NOT NULL,
    amount_paid DECIMAL(10,2) NOT NULL,
    payment_method ENUM('Cash', 'Card', 'Online') NOT NULL,
    payment_status ENUM('PAID', 'FAILED', 'REFUNDED') DEFAULT 'PAID',
    transaction_reference VARCHAR(100),
    paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
    ON DELETE CASCADE
);

#Inserting 
INSERT INTO payments 
(booking_id, amount_paid, payment_method, payment_status, transaction_reference)
VALUES 
(1, 25.00, 'Card', 'PAID', 'TXN123456'),
(2, 20.00, 'Cash', 'PAID', NULL);

#promotion table 
CREATE TABLE promotions (
    id INT PRIMARY KEY AUTO_INCREMENT, 
    promo_code VARCHAR (50) UNIQUE NOT NULL, 
    discount_percentage DECIMAL (5,2) NOT NULL, 
    valid_from DATE NOT NULL, 
    is_active BOOLEAN DEFAULT TRUE, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO promotions 
(promo_code, discount_percentage, valid_from, valid_to)
VALUES
('HORIZON10', 10.00, '2026-03-01', '2026-03-31'),
('VIP20', 20.00, '2026-03-05', '2026-04-01');

ALTER TABLE promotions
ADD COLUMN valid_to DATE NOT NULL;

ALTER TABLE booked_seats
ADD CONSTRAINT unique_seat_per_show UNIQUE (seat_id, booking_id);
 
 ALTER TABLE booked_seats
 ADD COLUMN show_id INT;
 
 CREATE INDEX idx_show_date ON shows(show_date); 
 CREATE INDEX inx_film_id ON shows (film_id);
 CREATE INDEX idx_user_id ON bookings(user_id);
 

#view all films and test queries 
SELECT * FROM films; 

SELECT 
    st.id, 
    f.name AS Film_Name, 
    st.show_date, 
    st.show_time,  
    st.base_price
FROM shows st  
JOIN films f ON st.film_id = f.id;
