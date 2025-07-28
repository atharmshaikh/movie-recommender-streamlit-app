import streamlit as st
import pickle
import difflib
import pandas as pd
import random

# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_titles = movies['title'].tolist()

def recommend(movie, top_n=5):
    movie = movie.strip().lower()
    matches = movies[movies['title'].str.lower() == movie]
    
    if matches.empty:
        # Find close match
        close_matches = difflib.get_close_matches(movie, movie_titles, n=1, cutoff=0.6)
        if close_matches:
            corrected_title = close_matches[0]
            st.warning(f"Did you mean **{corrected_title}**? Showing results for it.")
            matches = movies[movies['title'] == corrected_title]
        else:
            st.error("Movie not found. Please try another title.")
            return []

    idx = matches.index[0]
    distances = list(enumerate(similarity[idx]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)[1:top_n+1]
    recommended_movies = [movies.iloc[i[0]].title for i in distances]
    return recommended_movies

# Streamlit setup
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System")

# Pick a random default movie
if "default_movie" not in st.session_state:
    st.session_state.default_movie = random.choice(movie_titles)

# Input text with autocomplete dropdown
selected_movie = st.selectbox(
    "Type or select a movie title:",
    options=[""] + sorted(movie_titles),
    index=0,
    placeholder="Start typing to see suggestions...",
    key="movie_select"
)

# Clean input if pasted with quotes
if selected_movie:
    cleaned_movie = selected_movie.strip().replace('"', '').replace("'", "")
else:
    cleaned_movie = st.session_state.default_movie

# Small Enter button under input box
enter_clicked = st.button("Enter", key="enter_btn")

# Show recommendations on first load (default movie) or on click or on select
if cleaned_movie and (enter_clicked or selected_movie):
    rec_movies = recommend(cleaned_movie)
    if rec_movies:
        st.subheader(f"Top recommendations for **{cleaned_movie}**:")
        rec_cols = st.columns(5)
        for i, rec in enumerate(rec_movies):
            with rec_cols[i]:
                st.markdown(
                    f"""
                    <div style="background-color:#f0f0f5;
                                padding:20px;
                                border-radius:10px;
                                text-align:center;
                                font-size:16px;
                                font-weight:bold;
                                height:120px;
                                display:flex;
                                align-items:center;
                                justify-content:center;">
                        {rec}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
