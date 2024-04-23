import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('movie_booking.db')
cursor = conn.cursor()

# Function to retrieve available seats using SQL view
def get_available_seats():
    cursor.execute('SELECT * FROM AvailableSeats')
    return cursor.fetchall()

# Function to retrieve movie and show details using SQL join
def get_movie_and_show_details():
    cursor.execute('''
        SELECT m.title, m.genre, s.date, s.time, s.class, s.available_seats
        FROM Movies m
        JOIN Shows s ON m.id = s.movie_id
    ''')
    return cursor.fetchall()

# Commit changes and close connection
conn.commit()
conn.close()
