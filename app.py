import streamlit as st
import pickle
import numpy as np
import requests
import pandas as pd

import time
from requests.exceptions import ConnectionError


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=97ba66eeaeb4313ff8c52d09f42fc649&language=en-US"
    try:
        for attempt in range(3):  # Retry up to 3 times
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return "https://image.tmdb.org/t/p/w500/" + data.get('poster_path', None)
            time.sleep(2)  # Wait for 2 seconds before retrying
        st.error("Failed to fetch poster after several attempts.")
    except ConnectionError as e:
        st.error(f"Connection error: {e}")
    return None


def recommend(movie):
    movie_index = np.where(movies == movie)[0][0]
    distances = similarity[movie_index]
    movies_list_sorted = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies_posters = []
    recommended_movies = []
    for i in movies_list_sorted:
        movie_id = movies_list.iloc[i[0]]['movie_id']
        recommended_movies.append(movies[i[0]])
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

similarity = pickle.load(open('similarity.pickle','rb'))

st.title('Movie Recommender System')

movies_list = pickle.load(open('movies.pickle','rb'))
movies = movies_list['title'].values

selected_movie_name = st.selectbox(
    'select movie',
    movies
)


if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        if posters[0]:
            st.image(posters[0])
        else:
            st.text("Poster not available")

    with col2:
        st.text(names[1])
        if posters[1]:
            st.image(posters[1])
        else:
            st.text("Poster not available")

    with col3:
        st.text(names[2])
        if posters[2]:
            st.image(posters[2])
        else:
            st.text("Poster not available")

    with col4:
        st.text(names[3])
        if posters[3]:
            st.image(posters[3])
        else:
            st.text("Poster not available")

    with col5:
        st.text(names[4])
        if posters[4]:
            st.image(posters[4])
        else:
            st.text("Poster not available")


## to run: streamlit run "C:\Users\athar\PycharmProjects\Movie Recommender System\app.py"

##Api key TMDB : 97ba66eeaeb4313ff8c52d09f42fc649

## link: https://api.themoviedb.org/3/movie/{movie_id}?api_key=<<api_key>>&language=en-US


















# import pickle
# import streamlit as st
# import requests
#
# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path
#
# def recommend(movie):
#     index = movies[movies['title'] == movie].index[0]
#     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
#     recommended_movie_names = []
#     recommended_movie_posters = []
#     for i in distances[1:6]:
#         # fetch the movie poster
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movie_posters.append(fetch_poster(movie_id))
#         recommended_movie_names.append(movies.iloc[i[0]].title)
#
#     return recommended_movie_names,recommended_movie_posters
#
#
# st.header('Movie Recommender System')
# movies = pickle.load(open('movies.pickle','rb'))
# similarity = pickle.load(open('similarity.pickle','rb'))
#
# movie_list = movies['title'].values
# selected_movie = st.selectbox(
#     "Type or select a movie from the dropdown",
#     movie_list
# )
#
# if st.button('Show Recommendation'):
#     recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
#     col1, col2, col3, col4, col5 = st.beta_columns(5)
#     with col1:
#         st.text(recommended_movie_names[0])
#         st.image(recommended_movie_posters[0])
#     with col2:
#         st.text(recommended_movie_names[1])
#         st.image(recommended_movie_posters[1])
#
#     with col3:
#         st.text(recommended_movie_names[2])
#         st.image(recommended_movie_posters[2])
#     with col4:
#         st.text(recommended_movie_names[3])
#         st.image(recommended_movie_posters[3])
#     with col5:
#         st.text(recommended_movie_names[4])
#         st.image(recommended_movie_posters[4])




