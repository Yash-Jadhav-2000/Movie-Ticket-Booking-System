import streamlit as st
import pandas as pd

# Load the dataset
@st.cache_data()
def load_data():
    return pd.read_csv('movies.csv')

movies = load_data()

# Page title
st.title('Movie Ticket Booking App')

# Sidebar for selecting movie
selected_movie = st.sidebar.selectbox('Select a Movie', movies['Film'])

# Display selected movie details
selected_movie_details = movies[movies['Film'] == selected_movie].iloc[0]
st.subheader('Movie Details')
st.write(selected_movie_details)

# Select number of tickets
num_tickets = st.number_input('Select Number of Tickets', min_value=1, max_value=10, value=1)

# Display available seats
st.subheader('Available Seats')
available_seats_str = selected_movie_details['Worldwide Gross']
available_seats = float(available_seats_str.replace('$', '').replace(',', ''))  # Convert to float
st.write(f'Total available seats: {available_seats}')

# Button for booking tickets
if st.button('Book Tickets'):
    if available_seats >= num_tickets:
        updated_seats = available_seats - num_tickets
        movies.loc[movies['Film'] == selected_movie, 'Worldwide Gross'] = updated_seats
        movies.to_csv('movies.csv', index=False)
        st.success(f'{num_tickets} tickets booked for {selected_movie}!')
    else:
        st.error('Sorry, not enough seats available!')

# Display footer
st.sidebar.text('Created with Streamlit')
