import pickle
import streamlit as st
import requests

# Function to fetch movie poster using TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')  # Safely get poster_path
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"  # Return full URL
    return "https://via.placeholder.com/500"  # Return placeholder if poster is missing

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]  # Get the index of the selected movie
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])  # Sort by similarity
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:  # Fetch top 5 recommendations
        movie_id = movies.iloc[i[0]].id  # Use 'id' column #
        recommended_movie_names.append(movies.iloc[i[0]].title)  # Append movie title
        recommended_movie_posters.append(fetch_poster(movie_id))  # Append poster URL
    return recommended_movie_names, recommended_movie_posters

# Streamlit app header
st.header('Movie Recommender System')

# Load the data
movies = pickle.load(open('movie_list.pkl', 'rb'))  # Load movies DataFrame
similarity = pickle.load(open('similarity.pkl', 'rb'))  # Load similarity matrix

# Create a dropdown menu for movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Show recommendations when the button is clicked
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Display recommendations in 5 columns
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        if idx < len(recommended_movie_names):
            col.text(recommended_movie_names[idx])  # Display movie name
            col.image(recommended_movie_posters[idx])  # Display poster
