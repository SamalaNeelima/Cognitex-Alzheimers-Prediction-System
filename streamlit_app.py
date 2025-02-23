import os
import base64
import streamlit as st

# ✅ Set Page Configuration
st.set_page_config(
    page_title="Alzheimer's Prediction",
    page_icon="🧠",
    layout="wide"
)

# ✅ Import Other Pages
from streamlit_pages._home_page import home_page
from streamlit_pages._predict_alzheimer import prediction_page
from streamlit_pages._latest_news import news_page  
from streamlit_pages._chat_page import chat_bot


import sqlite3

# Connect to SQLite (or create it)
conn = sqlite3.connect("patients.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    contact TEXT NOT NULL,
    condition TEXT NOT NULL,
    image_path TEXT
)
''')

conn.commit()

# ✅ Set Background Video
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
BACKGROUND_VIDEO = os.path.join(ASSETS_DIR, "videos", "background.mp4")


def set_background_video(video_file):
    """Embed an MP4 video in the background."""
    if os.path.exists(video_file):
        video_base64 = get_base64_of_video(video_file)
        video_html = f"""
        <video autoplay loop muted playsinline class="background-video">
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>
        <style>
        .background-video {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            object-fit: cover;
            z-index: -1;
        }}
        </style>
        """
        st.markdown(video_html, unsafe_allow_html=True)


@st.cache_data()
def get_base64_of_video(video_path):
    """Convert a video file to base64 encoding."""
    try:
        with open(video_path, "rb") as file:
            return base64.b64encode(file.read()).decode("utf-8")
    except FileNotFoundError:
        st.error(f"🚨 Background video not found at: {video_path}")
        return ""


set_background_video(BACKGROUND_VIDEO)  # ✅ Set Background Video

# ✅ Horizontal Navigation Bar (Moved from Sidebar)
st.markdown("""
    <style>
        .navbar-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            padding: 12px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .navbar-button {
            font-size: 18px;
            font-weight: bold;
            padding: 10px 18px;
            border-radius: 8px;
            background: linear-gradient(135deg, #6e8efb, #a777e3);
            color: white;
            border: none;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        .navbar-button:hover {
            background: linear-gradient(135deg, #5a7ceb, #9a64d7);
        }
    </style>
""", unsafe_allow_html=True)

# ✅ Create Navigation Buttons (Top Navbar)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🏠 Home", key="home"):
        st.session_state["page"] = "Home"

with col2:
    if st.button("🔍 Predict", key="predict"):
        st.session_state["page"] = "Predict Alzheimer's"

with col3:
    if st.button("🤖 ChatBot", key="chatbot"):
        st.session_state["page"] = "ChatBot"

with col4:
    if st.button("📰 News", key="news"):
        st.session_state["page"] = "Latest News"



# ✅ Store Page Selection
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

# ✅ Display the Selected Page
if st.session_state["page"] == "Home":
    home_page()
elif st.session_state["page"] == "Predict Alzheimer's":
    prediction_page()
elif st.session_state["page"] == "ChatBot":
    chat_bot()
elif st.session_state["page"] == "Latest News":
    news_page()


# ✅ Sidebar (Only for Logo, Disclaimer, and Contact)
st.sidebar.image("assets/images/logo.webp")  # Change path if needed
st.sidebar.title("Cognitex: Alzheimer's Prediction System")

st.sidebar.write("""
### Disclaimer
The predictions provided by this system are for informational purposes only. Consult a healthcare professional for accurate diagnosis and advice.

### Contact
For inquiries, mail us [here](mailto:arpitsengar99@gmail.com).
""")
st.markdown("""
    <style>
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.2);  /* Adjust the opacity here */
            backdrop-filter: blur(10px); /* Adds a slight blur effect */
            padding: 20px;
            border-radius: 15px;
        }
    </style>
""", unsafe_allow_html=True)

