import streamlit as st
import pickle
import numpy as np
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import time

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
        margin-bottom: 2rem;
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

    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #FF416C 0%, #8A2387 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1.05rem;
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
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

def get_http_session():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

@st.cache_data(show_spinner=False)
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        session = get_http_session()
        response = session.get(url, headers=HEADERS, timeout=5)
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
    except Exception:
        pass
    return {
        "poster": "https://via.placeholder.com/500x750/1a1a2e/ffffff?text=No+Poster",
        "rating": "N/A",
        "year": "N/A",
        "overview": ""
    }

@st.cache_data(show_spinner=False)
def search_tmdb_live(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&language=en-US"
    try:
        session = get_http_session()
        response = session.get(url, headers=HEADERS, timeout=5)
        if response.status_code == 200:
            return response.json().get('results', [])[:10]
    except Exception:
        pass
    return []

@st.cache_data(show_spinner=False)
def fetch_tmdb_recommendations(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={TMDB_API_KEY}&language=en-US"
    try:
        session = get_http_session()
        response = session.get(url, headers=HEADERS, timeout=5)
        if response.status_code == 200:
            results = response.json().get('results', [])[:5]
            recs = []
            for item in results:
                poster_path = item.get('poster_path')
                poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750/1a1a2e/ffffff?text=No+Poster"
                recs.append({
                    "title": item.get('title', 'Unknown Title'),
                    "poster": poster_url,
                    "rating": round(item.get('vote_average', 0.0), 1),
                    "year": item.get('release_date', '')[:4] if item.get('release_date') else "N/A",
                    "overview": item.get('overview', 'No overview available.')
                })
            return recs
    except Exception:
        pass
    return []

@st.cache_resource(show_spinner=False)
def load_data():
    try:
        movies_list = pickle.load(open('movies.pickle', 'rb'))
        try:
            top_recs = pickle.load(open('top_recs.pkl', 'rb'))
            return movies_list, top_recs, "top_recs"
        except FileNotFoundError:
            pass

        try:
            similarity = pickle.load(open('similarity_f16.pkl', 'rb'))
        except FileNotFoundError:
            similarity = pickle.load(open('similarity.pickle', 'rb'))
        return movies_list, similarity, "matrix"
    except Exception as e:
        return None, None, None

def recommend_ml(movie, movies_list, data, mode):
    movies = movies_list['title'].values
    recommended_movies = []

    if mode == "top_recs":
        movie_ids = data.get(movie, [])[:5]
        for m_id in movie_ids:
            matching_rows = movies_list[movies_list['movie_id'] == m_id]
            title = matching_rows.iloc[0]['title'] if not matching_rows.empty else "Unknown Movie"
            details = fetch_movie_details(m_id)
            recommended_movies.append({
                "title": title,
                "poster": details["poster"],
                "rating": details["rating"],
                "year": details["year"],
                "overview": details["overview"]
            })
    else:
        movie_index = np.where(movies == movie)[0][0]
        distances = data[movie_index]
        movies_list_sorted = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        for i in movies_list_sorted:
            m_id = movies_list.iloc[i[0]]['movie_id']
            title = movies[i[0]]
            details = fetch_movie_details(m_id)
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
st.markdown('<div class="subtitle">Content Similarity Engine & Live Global Movie Discovery</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🧠 Trained ML Model (4,800+ Movies)", "🌐 Live Global Search (Any Movie up to 2026)"])

with tab1:
    movies_list, data, mode = load_data()
    if movies_list is not None and data is not None:
        movies = movies_list['title'].values

        col_select1, col_select2, col_select3 = st.columns([1, 2, 1])
        with col_select2:
            selected_movie_name = st.selectbox(
                "Select a movie from trained ML dataset:",
                movies,
                index=list(movies).index("Avatar") if "Avatar" in movies else 0,
                key="ml_select"
            )
            recommend_btn = st.button("✨ Discover Similar Movies", key="ml_btn")

        if recommend_btn:
            with st.spinner("Analyzing cinematic DNA & fetching live metadata..."):
                recs = recommend_ml(selected_movie_name, movies_list, data, mode)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"### 🍿 Top Recommendations for **{selected_movie_name}**")
            st.markdown("<br>", unsafe_allow_html=True)

            cols = st.columns(5)
            for idx, col in enumerate(cols):
                rec = recs[idx]
                with col:
                    st.image(rec["poster"], use_column_width=True)
                    st.markdown(f"**{rec['title']}**")
                    st.caption(f"⭐ {rec['rating']} / 10  •  📅 {rec['year']}")
                    with st.expander("Storyline"):
                        st.write(rec["overview"])
    else:
        st.warning("Please ensure `movies.pickle` and data files are present.")

with tab2:
    col_s1, col_s2, col_s3 = st.columns([1, 2, 1])
    with col_s2:
        search_query = st.text_input("Type ANY movie title (e.g., Obsession, Dune Part Two, Oppenheimer):", placeholder="Enter movie title...")
        search_btn = st.button("🔍 Search & Recommend Live", key="live_btn")

    if search_query and (search_btn or search_query):
        with st.spinner(f"Searching global TMDB database for '{search_query}'..."):
            results = search_tmdb_live(search_query)

        if results:
            first_movie = results[0]
            movie_id = first_movie['id']
            title = first_movie['title']
            year = first_movie.get('release_date', '')[:4] if first_movie.get('release_date') else "N/A"

            st.success(f"Found Match: **{title} ({year})** — fetching global recommendations...")
            recs = fetch_tmdb_recommendations(movie_id)

            if recs:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"### 🌐 Global Recommendations for **{title} ({year})**")
                st.markdown("<br>", unsafe_allow_html=True)

                cols = st.columns(len(recs))
                for idx, col in enumerate(cols):
                    rec = recs[idx]
                    with col:
                        st.image(rec["poster"], use_column_width=True)
                        st.markdown(f"**{rec['title']}**")
                        st.caption(f"⭐ {rec['rating']} / 10  •  📅 {rec['year']}")
                        with st.expander("Storyline"):
                            st.write(rec["overview"])
            else:
                st.info("No direct recommendations found for this movie yet.")
        else:
            st.warning(f"Could not find any movie matching '{search_query}' on TMDB.")
