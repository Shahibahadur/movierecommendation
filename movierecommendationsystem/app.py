import pickle
import streamlit as st
import requests
import os
from dotenv import load_dotenv
from config import initialize_database, get_db_connection
from auth import login_user, register_user, get_user_info

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

if not API_KEY:
    st.error("TMDB API key not found. Please add it to your .env file.")
    st.stop()

# Initialize database on app startup
initialize_database()

# Initialize session state for authentication
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None

# Function to fetch movie poster
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=Error"

# Function to get movie recommendations
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Login and Registration Page
def show_login_page():
    st.set_page_config(page_title="Movie Recommender - Login", layout="wide")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.title("🎬 Movie Recommender")
        st.write("Discover your next favorite movie!")
    
    with col2:
        st.write("")
        st.write("")
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.subheader("Login")
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", use_container_width=True):
                if not login_username or not login_password:
                    st.error("Please enter both username and password")
                else:
                    success, user_id, message = login_user(login_username, login_password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.username = login_username
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        
        with tab2:
            st.subheader("Create New Account")
            signup_username = st.text_input("Choose Username", key="signup_username")
            signup_email = st.text_input("Email Address", key="signup_email")
            signup_password = st.text_input("Password", type="password", key="signup_password")
            signup_password_confirm = st.text_input("Confirm Password", type="password", key="signup_password_confirm")
            
            if st.button("Sign Up", use_container_width=True):
                if not signup_username or not signup_email or not signup_password:
                    st.error("Please fill in all fields")
                elif signup_password != signup_password_confirm:
                    st.error("Passwords do not match")
                else:
                    success, message = register_user(signup_username, signup_email, signup_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

# Main Recommendation Page
def show_main_page():
    st.set_page_config(page_title="Movie Recommender System", layout="wide")
    
    # Sidebar
    with st.sidebar:
        st.title("🎬 Movie Recommender")
        
        # User info
        user_info = get_user_info(st.session_state.user_id)
        if user_info:
            st.write(f"Welcome, **{user_info['username']}**!")
            st.write(f"📧 {user_info['email']}")
            st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()
    
    # Main content
    st.header('🎬 Movie Recommender System')
    st.write("Select a movie and get personalized recommendations!")
    
    # Load data
    movies = pickle.load(open('movie_list.pkl','rb'))
    similarity = pickle.load(open('similarity.pkl','rb'))

    movie_list = movies['title'].values
    selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

    if st.button('Show Recommendation', use_container_width=True):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        
        st.subheader(f"Movies similar to '{selected_movie}':")
        
        # Dynamically create columns
        cols = st.columns(len(recommended_movie_names))
        for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
            with col:
                st.image(poster)
                st.text(name)

# Main app logic
if st.session_state.logged_in:
    show_main_page()
else:
    show_login_page()
