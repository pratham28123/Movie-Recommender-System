

import streamlit as st
import pickle
import pandas as pd



def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies


def recommend_by_genre(genre, num_recommendations=5):
    # Get random movies as recommendations
    recommendations = movies['title'].sample(num_recommendations).tolist()
    return recommendations


# Load data
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

st.title("Movie Recommender System")

# Create tabs for different recommendation methods
tab_selection = st.radio(
    "Choose Recommendation Method:",
    ["Recommend by Movie", "Recommend by Genre"]
)

if tab_selection == "Recommend by Movie":
    st.header("Movie-based Recommendations")
    selected_movie_name = st.selectbox(
        "Which movie would you like to watch?",
        movies["title"].values,
    )

    if st.button("Recommend Movies"):
        with st.spinner('Finding recommendations...'):
            recommendations = recommend(selected_movie_name)
            st.subheader("Recommended Movies:")
            for i, movie in enumerate(recommendations, 1):
                st.write(f"{i}. {movie}")

else:  # Genre-based recommendations
    st.header("Genre-based Recommendations")

    # Predefined list of common movie genres
    genre_list = [
        "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
        "Drama", "Family", "Fantasy", "Horror", "Mystery", "Romance",
        "Science Fiction", "Thriller", "War"
    ]

    selected_genre = st.selectbox(
        "Select a genre:",
        genre_list
    )

    num_recommendations = st.slider(
        "Number of recommendations:",
        min_value=1,
        max_value=10,
        value=5
    )

    if st.button("Get Genre Recommendations"):
        with st.spinner('Finding genre-based recommendations...'):
            genre_recommendations = recommend_by_genre(selected_genre, num_recommendations)
            if genre_recommendations:
                st.subheader(f"Top {num_recommendations} {selected_genre} Movies:")
                for i, movie in enumerate(genre_recommendations, 1):
                    st.write(f"{i}. {movie}")
            else:
                st.error(f"No movies found for the genre: {selected_genre}")

# Add some styling
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        margin-top: 10px;
    }
    .stSelectbox {
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Footer
st.markdown("-----")
st.markdown("""
    <div style="text-align: center">
        <h3>Movie Recommender System</h3>
        <p>Developed by Pratham Kumar Singh</p>
        <p>© 2024 All Rights Reserved</p>
        <p>Contact: prathamkumarsingh@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)