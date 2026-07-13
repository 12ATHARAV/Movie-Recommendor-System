import streamlit as st
import pickle
import numpy as np
import requests
import pandas as pd
import time
from requests.exceptions import ConnectionError

# Configure page aesthetic
st.set_page_config(
    page_title="CineAI | Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Cinema Premium Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    .main-title {
        background: linear-gradient(135deg, #FF416C 0%, #8A2387 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        text-align: center;
        color: #A0AEC0;
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
    }

    .movie-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 12px;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }

    .movie-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 28px rgba(255, 65, 108, 0.25);
        border-color: rgba(255, 65, 108, 0.5);
    }

    .movie-title {
        font-size: 1rem;
        font-weight: 600;
        color: #F7FAFC;
        margin-top: 10px;
        min-height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .movie-meta {
        font-size: 0.85rem;
        color: #CBD5E0;
        margin-top: 4px;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #FF416C 0%, #8A2387 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        box-shadow: 0 8px 20px rgba(255, 65, 108, 0.4);
        transform: scale(1.01);
    }
</style>
""", unsafe_allow_html=True)

TMDB_API_KEY = "97ba66eeaeb4313ff8c52d09f42fc649"

@st.cache_data(show_spinner=False)
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        for _ in range(2):
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                poster_path = data.get('poster_path')
                poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750/1a1a2e/ffffff?text=No+Poster"
                rating = round(data.get('vote_average', 0.0), 1)
                year = data.get('release_date', '')[:4] if data.get('release_date') else "N/A"
                overview = data.get('overview', 'No overview available.')
                return {
                    "poster": poster_url,
                    "rating": rating,
                    "year": year,
                    "overview": overview
                }
            time.sleep(0.5)
    except Exception:
        pass
    return {
        "poster": "https://via.placeholder.com/500x750/1a1a2e/ffffff?text=No+Poster",
        "rating": "N/A",
        "year": "N/A",
        "overview": ""
    }

@st.cache_resource(show_spinner=False)
def load_data():
    try:
        # Try loading float16 version first, fallback to standard
        try:
            similarity = pickle.load(open('similarity_f16.pkl', 'rb'))
        except FileNotFoundError:
            similarity = pickle.load(open('similarity.pickle', 'rb'))
        movies_list = pickle.load(open('movies.pickle', 'rb'))
        return movies_list, similarity
    except Exception as e:
        st.error(f"Error loading model files: {e}")
        return None, None

def recommend(movie, movies_list, similarity):
    movies = movies_list['title'].values
    movie_index = np.where(movies == movie)[0][0]
    distances = similarity[movie_index]
    movies_list_sorted = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list_sorted:
        movie_id = movies_list.iloc[i[0]]['movie_id']
        title = movies[i[0]]
        details = fetch_movie_details(movie_id)
        recommended_movies.append({
            "title": title,
            "poster": details["poster"],
            "rating": details["rating"],
            "year": details["year"],
            "overview": details["overview"]
        })
    return recommended_movies

# Header
st.markdown('<div class="main-title">🎬 CineAI Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Powered Content Similarity Engine using Cosine Similarity & TMDB Live Data</div>', unsafe_allow_html=True)

movies_list, similarity = load_data()

if movies_list is not None and similarity is not None:
    movies = movies_list['title'].values

    col_select1, col_select2, col_select3 = st.columns([1, 2, 1])
    with col_select2:
        selected_movie_name = st.selectbox(
            "Choose a movie you love:",
            movies,
            index=list(movies).index("Avatar") if "Avatar" in movies else 0
        )
        recommend_btn = st.button("✨ Discover Similar Movies")

    if recommend_btn:
        with st.spinner("Analyzing cinematic DNA & fetching live metadata..."):
            recs = recommend(selected_movie_name, movies_list, similarity)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"### 🍿 Top Recommendations for **{selected_movie_name}**")
        st.markdown("<br>", unsafe_allow_html=True)

        cols = st.columns(5)
        for idx, col in enumerate(cols):
            rec = recs[idx]
            with col:
                st.image(rec["poster"], use_container_width=True)
                st.markdown(f"**{rec['title']}**")
                st.caption(f"⭐ {rec['rating']} / 10  •  📅 {rec['year']}")
                with st.expander("Storyline"):
                    st.write(rec["overview"])
else:
    st.warning("Please ensure `movies.pickle` and `similarity.pickle` are present in the app directory.")
