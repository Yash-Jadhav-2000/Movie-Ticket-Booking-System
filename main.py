import streamlit as st
import pandas as pd

# Load the dataset
@st.cache_data()
def load_data():
    # Read the CSV file and automatically fix column types
    return pd.read_csv('movies.csv', dtype={'Seats Available': str})

def book_tickets(selected_movie, num_tickets):
    movies = load_data()
    selected_movie_details = movies[movies['Film'] == selected_movie].iloc[0]
    available_seats_str = selected_movie_details['Seats Available']
    available_seats_list = available_seats_str.split(", ")
    
    if len(available_seats_list) >= num_tickets:
        updated_seats = ", ".join(available_seats_list[num_tickets:])
        movies.loc[movies['Film'] == selected_movie, 'Seats Available'] = updated_seats
        movies.to_csv('movies.csv', index=False)
        return True
    else:
        return False

# Page title
st.title('Movie Ticket Booking App')

# Page selection
page = st.sidebar.radio("Select a page", ["Home", "Available Seats"])

if page == "Home":
    movies = load_data()
    # Display list of movies as buttons
    st.subheader('List of Movies')
    for index, movie in movies.iterrows():
        if st.button(movie['Film']):
            selected_movie = movie['Film']
            page = "Book Tickets"
            break

elif page == "Available Seats":
    # Display available seats for all movies
    st.subheader('Available Seats')
    movies = load_data()
    for index, movie in movies.iterrows():
        st.write(f"Movie: {movie['Film']}")
        st.write(f"Available Seats: {movie['Seats Available']}")

if page == "Book Tickets":
    # Display selected movie details
    st.subheader('Movie Details')
    selected_movie_details = movies[movies['Film'] == selected_movie].iloc[0]
    st.write(selected_movie_details)

    # Display available seats
    st.subheader('Available Seats')
    available_seats_str = selected_movie_details['Seats Available']
    available_seats_list = available_seats_str.split(", ")
    st.write(f'Total available seats: {len(available_seats_list)}')

    # Select number of tickets
    num_tickets = st.number_input('Select Number of Tickets', min_value=1, max_value=len(available_seats_list), value=1)

    # Button for booking tickets
    if st.button('Book Tickets'):
        if book_tickets(selected_movie, num_tickets):
            st.success(f'{num_tickets} tickets booked for {selected_movie}!')
        else:
            st.error('Sorry, not enough seats available!')

    # Show booked tickets for the selected movie
    booked_tickets_str = selected_movie_details['Seats Available']
    if booked_tickets_str:
        booked_tickets_list = booked_tickets_str.split(", ")
        booked_tickets_count = len(booked_tickets_list) - len(available_seats_list)
        st.subheader('Your Booked Tickets')
        st.write(f'You have booked {booked_tickets_count} tickets for {selected_movie}')

# Display footer
st.sidebar.text('Created with Streamlit')
