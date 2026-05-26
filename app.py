import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=bbfda3bcb88de65635c89f04673b0ecf&language=en-US"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return "https://via.placeholder.com/500x750?text=No+Image"

        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except:
        return "https://via.placeholder.com/500x750?text=No+Image"
    
def recommend(movie):
    movie_index = list(movies_list).index(movie)
    distances = similarity[movie_index]
    
    similar_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in similar_movies:
        movie_id = movies.iloc[i[0]].movie_id

        poster = fetch_poster(movie_id)
        recommended_movies_posters.append(poster)

        recommended_movies.append(movies_list[i[0]])
    
    return recommended_movies, recommended_movies_posters
movies = pickle.load(open('movies.pkl','rb'))
movies_list = movies['title'].values

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies_list
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header(names[0])
        if posters[0]:
            st.image(posters[0])
        else:
            st.write("No Image Available")

    with col2:
        st.header(names[1])
        if posters[1]:
            st.image(posters[1])
        else:
            st.write("No Image Available")

    with col3:
        st.header(names[2])
        if posters[2]:
            st.image(posters[2])
        else:
            st.write("No Image Available")