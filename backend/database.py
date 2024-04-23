import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('movie_booking.db')
cursor = conn.cursor()

# Create tables if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS CinemaHalls (
        id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        screens INTEGER,
        capacity_per_screen INTEGER,
        rate_per_screen REAL,
        facilities TEXT,
        location_map TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Movies (
        id INTEGER PRIMARY KEY,
        title TEXT,
        duration INTEGER,
        genre TEXT,
        rating REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Shows (
        id INTEGER PRIMARY KEY,
        movie_id INTEGER,
        hall_id INTEGER,
        date TEXT,
        time TEXT,
        class TEXT,
        available_seats INTEGER,
        FOREIGN KEY(movie_id) REFERENCES Movies(id),
        FOREIGN KEY(hall_id) REFERENCES CinemaHalls(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Bookings (
        id INTEGER PRIMARY KEY,
        show_id INTEGER,
        user_id INTEGER,
        seats_booked INTEGER,
        total_amount REAL,
        mode_of_transfer TEXT,
        booking_date TEXT,
        FOREIGN KEY(show_id) REFERENCES Shows(id)
    )
''')

# Create SQL views
cursor.execute('''
    CREATE VIEW IF NOT EXISTS AvailableSeats AS
    SELECT s.id AS show_id, s.date, s.time, s.class, s.available_seats, c.name AS cinema_hall
    FROM Shows s
    JOIN CinemaHalls c ON s.hall_id = c.id;
''')

# Commit changes and close connection
conn.commit()
conn.close()
