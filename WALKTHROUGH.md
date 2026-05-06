# Horizon Cinemas Booking System - Complete Walkthrough

Welcome! This guide walks you through the entire codebase so you understand how everything works together.

---

## 📋 Project Overview

**Horizon Cinemas Booking System (HCBS)** is a desktop cinema booking application built with Python and SQLite. It allows customers to browse films, select shows, book seats, and manage bookings. Admins and managers can manage cinemas, films, and shows.

### Key Features
- **Customer**: Browse films, select shows, book seats, view bookings, cancel bookings
- **Admin**: Add/edit cinemas, films, shows, cities, users, screen configurations
- **Manager**: View cinema operations, manage shows and bookings
- **Authentication**: Role-based user login (Admin, Manager, Customer)

---

## 🏗️ Architecture Overview

The application follows a **layered architecture**:

```
GUI Layer (tkinter)
    ↓
Controllers (Business Logic)
    ↓
Services (Data Processing)
    ↓
Repositories (Database Access)
    ↓
Models (Data Objects)
    ↓
Database (SQLite)
```

Each layer has a clear responsibility:
- **Models**: Data structures (Python classes representing database entities)
- **Repositories**: Database operations (CRUD queries)
- **Services**: Business logic and validation
- **Controllers**: Orchestrate repositories and services
- **GUI**: User interface and user interactions

---

## 📁 Project Structure

```
ASD_Ayusha_Poudel_24036546/
├── app/                          # Main application code
│   ├── __init__.py
│   ├── models/                   # Data models
│   │   ├── user.py              # User class (id, username, password, role)
│   │   ├── city.py              # City class
│   │   ├── cinema.py            # Cinema class (cinema, city, address)
│   │   ├── film.py              # Film class (name, genre, duration)
│   │   ├── screen.py            # Screen class (cinema, screen number, capacity)
│   │   ├── seat.py              # Seat class (row, number, type: regular/vip)
│   │   ├── show.py              # Show class (film, cinema, time, price)
│   │   └── booking.py           # Booking class (user, show, reference, status)
│   │
│   ├── repositories/             # Database access layer
│   │   ├── user_repository.py    # get_user_by_username, add_user, etc.
│   │   ├── city_repository.py    # add_city, delete_city, update_city
│   │   ├── cinema_repository.py  # cinema CRUD operations
│   │   ├── film_repository.py    # film CRUD operations
│   │   ├── screen_repository.py  # screen CRUD operations
│   │   ├── seat_repository.py    # seat CRUD operations
│   │   ├── show_repository.py    # show CRUD operations
│   │   └── booking_repository.py # booking CRUD operations
│   │
│   ├── services/                 # Business logic
│   │   └── user_service.py       # Authenticate users, validate credentials
│   │
│   └── controllers/              # Coordination layer
│       ├── admin_controller.py   # Orchestrates all repositories for admin tasks
│       └── auth_controller.py    # Handles authentication
│
├── config/                        # Configuration
│   ├── __init__.py
│   └── database.py               # Database connection setup
│
├── gui/                          # User interface (tkinter)
│   ├── loginWindow.py            # Login screen
│   ├── customer_panel.py         # Customer booking interface
│   ├── admin_panal.py            # Admin panel (note: typo "panal" kept for consistency)
│   ├── manager_panal.py          # Manager panel
│   ├── theme.py                  # UI theming
│   └── __init__.py
│
├── tests/                        # Unit tests
│   ├── test_base.py              # Base test class with database setup
│   ├── test_models.py            # Model unit tests
│   ├── test_repositories.py      # Repository unit tests
│   └── __init__.py
│
├── .circleci/                    # CI/CD configuration
│   └── config.yml                # CircleCI pipeline configuration
│
├── horizon_db.sql                # Database schema (CREATE TABLE statements)
├── horizon_db.sqlite3            # Actual database (created after first run)
├── requirements.txt              # Python dependencies (empty - uses stdlib only)
├── run.py                        # Application entry point
├── run_tests.py                  # Test runner
└── README.md                     # Quick start guide
```

---

## 🗄️ Database Schema

The database has 8 main tables:

### 1. **users**
Stores user accounts with roles.
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL  -- 'admin', 'manager', 'customer'
);
```

### 2. **cities**
Cities where cinemas are located.
```sql
CREATE TABLE cities (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);
```

### 3. **cinemas**
Cinema chains/locations.
```sql
CREATE TABLE cinemas (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city_id INTEGER,
    address TEXT,
    FOREIGN KEY (city_id) REFERENCES cities(id)
);
```

### 4. **films**
Film catalog.
```sql
CREATE TABLE films (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    genre TEXT,
    duration INTEGER  -- minutes
);
```

### 5. **screens**
Screens within cinemas.
```sql
CREATE TABLE screens (
    id INTEGER PRIMARY KEY,
    cinema_id INTEGER NOT NULL,
    screen_number INTEGER,
    capacity INTEGER,  -- total seats
    FOREIGN KEY (cinema_id) REFERENCES cinemas(id)
);
```

### 6. **seats**
Physical seats in screens.
```sql
CREATE TABLE seats (
    id INTEGER PRIMARY KEY,
    screen_id INTEGER NOT NULL,
    row CHAR(1),      -- A, B, C, etc.
    number INTEGER,
    type TEXT,        -- 'regular' or 'vip'
    FOREIGN KEY (screen_id) REFERENCES screens(id)
);
```

### 7. **shows**
Film showtimes.
```sql
CREATE TABLE shows (
    id INTEGER PRIMARY KEY,
    film_id INTEGER NOT NULL,
    cinema_id INTEGER NOT NULL,
    show_time TEXT,   -- datetime string
    price REAL,
    FOREIGN KEY (film_id) REFERENCES films(id),
    FOREIGN KEY (cinema_id) REFERENCES cinemas(id)
);
```

### 8. **bookings**
Customer bookings (can have multiple seats per booking).
```sql
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    show_id INTEGER NOT NULL,
    booking_reference TEXT UNIQUE,
    status TEXT DEFAULT 'confirmed',  -- 'confirmed', 'cancelled'
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (show_id) REFERENCES shows(id)
);
```

### 9. **booked_seats** (Junction table)
Maps seats to bookings (one booking can reserve multiple seats).
```sql
CREATE TABLE booked_seats (
    id INTEGER PRIMARY KEY,
    booking_id INTEGER NOT NULL,
    seat_id INTEGER NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES bookings(id),
    FOREIGN KEY (seat_id) REFERENCES seats(id)
);
```

---

## 🔄 Data Flow Example: Customer Books a Seat

Here's how data flows through the layers when a customer books a show:

```
1. GUI: Customer clicks "Book Seat" button
   ↓
2. GUI Handler: Collects show_id, seat_id, user_id from form
   ↓
3. Controller: controller.add_booking(booking_model)
   ↓
4. Repository: booking_repo.add_booking(booking)
   ↓
5. Database: INSERT INTO bookings (...) VALUES (...)
   ↓
6. Response: booking_id returned to controller
   ↓
7. Controller: Returns booking_id to GUI
   ↓
8. GUI: Shows confirmation "Booking Reference: #12345"
```

**Example Code Path:**
```python
# GUI calls:
booking = Booking(user_id=1, show_id=5, booking_reference="REF001")
booking_id = self.controller.add_booking(booking)

# Controller does:
def add_booking(self, booking):
    return self.booking_repo.add_booking(booking)

# Repository does:
def add_booking(self, booking):
    cursor.execute(
        "INSERT INTO bookings (user_id, show_id, booking_reference, status) VALUES (?, ?, ?, ?)",
        (booking.user_id, booking.show_id, booking.booking_reference, booking.status)
    )
    return cursor.lastrowid
```

---

## 🔐 Authentication Flow

1. **Login Screen** (`gui/loginWindow.py`):
   - User enters username and password
   - Calls `auth_controller.login(username, password)`

2. **Auth Controller** (`app/controllers/auth_controller.py`):
   - Calls `user_service.authenticate_user(username, password)`

3. **User Service** (`app/services/user_service.py`):
   - Calls `user_repo.get_user_by_username(username)`
   - Compares stored password with input
   - Returns User object if match, None otherwise
   - **Security Note**: Passwords are compared directly (should use hashing in production)

4. **GUI Response**:
   - If authenticated, load appropriate panel (Admin/Manager/Customer)
   - If not, show error message

---

## 🧩 Key Components Explained

### Models (`app/models/`)

Models are simple data classes:

```python
# Example: User Model
class User:
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role  # 'admin', 'manager', 'customer'
```

### Repositories (`app/repositories/`)

Repositories handle all database queries:

```python
# Example: Get all cities
def get_all_cities(self):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM cities")
    results = cursor.fetchall()
    cities = []
    for row in results:
        cities.append(City(id=row['id'], name=row['name']))
    return cities
```

### Services (`app/services/`)

Services implement business logic:

```python
# Example: Authenticate user
def authenticate_user(self, username, password):
    user = self.user_repo.get_user_by_username(username)
    if user and user.password == password:
        return user
    return None
```

### Controllers (`app/controllers/`)

Controllers coordinate repositories and services:

```python
# Example: Admin controller
class AdminController:
    def __init__(self):
        self.user_repo = UserRepository()
        self.cinema_repo = CinemaRepository()
        # ... other repositories
    
    def add_city(self, city_name):
        return self.city_repo.add_city(city_name)
```

---

## 🖥️ GUI Layers

### Login Window (`gui/loginWindow.py`)
- Entry points: username and password fields
- Buttons: Login, Register
- Connects to `auth_controller`

### Customer Panel (`gui/customer_panel.py`)
- Browse films and shows
- Select seats and book
- View booking history
- Cancel bookings

### Admin Panel (`gui/admin_panal.py`)
- Add/Edit/Delete cities, cinemas, films, shows, screens, seats
- Manage users
- View all bookings

### Manager Panel (`gui/manager_panal.py`)
- View cinema operations
- Monitor shows and bookings

---

## 🧪 Testing

### Test Structure

Tests are organized in `tests/` directory:

1. **test_base.py**: Base class for all tests
   - Sets up a temporary test database
   - Initializes schema from `horizon_db.sql`
   - Cleans up after each test

2. **test_models.py**: Model unit tests
   - Tests model creation and attributes
   - Example: `test_user_model()` creates User and checks fields

3. **test_repositories.py**: Repository unit tests
   - Tests CRUD operations on database
   - Example: `test_city_repository_add()` adds a city and verifies insertion

### Running Tests

```bash
python run_tests.py
```

**Output:**
```
Ran 41 tests in 18.154s
OK
```

---

## ⚙️ Recent Fixes & Improvements

### 1. ✅ Fixed AttributeError in City Addition
**Problem**: `admin_controller.add_city(name)` passed a string, but `city_repository.add_city()` expected a City object.

**Solution**: Updated `city_repository.add_city()` to accept both strings and City objects:
```python
def add_city(self, city):
    if isinstance(city, str):
        name = city
    else:
        name = city.name
    cursor.execute(query, (name,))
```

### 2. ✅ Removed Sensitive Console Logs
**Problem**: Authentication flow printed password comparisons to console:
```
"Found user. Comparing: 'password123' == 'input_password'"
```

**Solution**: Replaced with non-sensitive debug logging:
```python
import logging
logger.debug("Found user; verifying password for user: %s", username)
```

### 3. ✅ Fixed Test Database Path Resolution
**Problem**: `test_base.py` used relative path `"horizon_db.sql"`, which failed in CI/CD environments.

**Solution**: Construct path relative to project root:
```python
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sql_file = os.path.join(project_root, "horizon_db.sql")
```

---

## 🔄 CI/CD Pipeline (CircleCI)

CircleCI automatically runs tests on every push:

```yaml
# .circleci/config.yml
jobs:
  build-and-test:
    docker:
      - image: cimg/python:3.12
    steps:
      - checkout
      - install-dependencies
      - run: python run_tests.py
```

**How it works:**
1. Code pushed to GitHub
2. CircleCI detects `.circleci/config.yml`
3. Starts Python 3.12 Docker container
4. Runs `python run_tests.py`
5. Reports pass/fail status

---

## 🚀 How to Run the Application

### Setup (One-time)

```bash
# 1. Create virtual environment (optional)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Initialize database (if first run)
python -c "import sqlite3; sql = open('horizon_db.sql').read(); conn = sqlite3.connect('horizon_db.sqlite3'); conn.executescript(sql); conn.close(); print('DB created')"

# 3. Run app
python run.py
```

### Login Credentials

**Admin:**
- Username: `admin`
- Password: `admin123`

**Manager:**
- Username: `manager1`
- Password: `manager123`

**Customer:**
- Username: `customer1`
- Password: `customer123`

---

## 🐛 Debugging Tips

### Enable Debug Logging

```python
# In any file
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

### Check Database State

```bash
# Open database directly
sqlite3 horizon_db.sqlite3

# View all tables
.tables

# Query data
SELECT * FROM users;
SELECT * FROM bookings;
```

### Run Specific Test

```bash
python -m unittest tests.test_repositories.TestRepositories.test_city_repository_add -v
```

---

## 📝 Code Standards

### Naming Conventions
- **Classes**: PascalCase (`User`, `Cinema`, `Booking`)
- **Functions**: snake_case (`add_booking()`, `get_all_cities()`)
- **Variables**: snake_case (`user_id`, `cinema_name`)
- **Constants**: UPPER_SNAKE_CASE (rarely used)

### File Organization
- One class per file in models and repositories
- Multiple related functions in services
- Controllers group related operations

### Documentation
- Add comments for complex logic
- Use docstrings for public methods (optional but recommended)
- Log important operations at debug level

---

## 🤝 Contributing

When making changes:

1. **Create a feature branch**: `git checkout -b feature/my-feature`
2. **Make changes following the architecture**
3. **Run tests**: `python run_tests.py`
4. **Commit with clear messages**: `git commit -m "Add new feature"`
5. **Push and create Pull Request**: `git push origin feature/my-feature`

---

## 📚 Next Steps

Now that you understand the architecture:

1. **Explore the models** (`app/models/`) - Understand the data structures
2. **Look at repositories** (`app/repositories/`) - See how data is persisted
3. **Review controllers** (`app/controllers/`) - Understand orchestration
4. **Check the GUI** (`gui/`) - See how users interact with the system
5. **Run tests** - Verify everything works
6. **Try the app** - Use `python run.py` to interact with it

Happy coding! 🎬
