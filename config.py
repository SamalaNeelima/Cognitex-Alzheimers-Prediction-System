import os
import streamlit as st
import base64

# ✅ Get Absolute Path for Assets Directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Gets the directory of streamlit_app.py
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
VIDEO_PATH = os.path.join(ASSETS_DIR, "videos", "background.mp4")

# ✅ Load CSS File
CSS_PATH = os.path.join(ASSETS_DIR, "css", "styles.css")
try:
    with open(CSS_PATH, "r") as file:
        CSS = file.read()
except FileNotFoundError:
    CSS = ""  # Default empty CSS if file is missing

# ✅ Apply CSS to Streamlit
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

# ✅ ASSETS - Absolute Paths for Images
BANNER = os.path.join(ASSETS_DIR, "images", "banner.webp")
DEFAULT_IMAGE = os.path.join(ASSETS_DIR, "images", "logo.webp")
SIDE_BANNER = os.path.join(ASSETS_DIR, "images", "logo.webp")
EMOJI = os.path.join(ASSETS_DIR, "images", "emo.webp")

@st.cache_data()
def video_to_base64(video_path):
    """Convert a video file to base64 encoding for embedding in HTML."""
    try:
        with open(video_path, "rb") as video_file:
            return base64.b64encode(video_file.read()).decode("utf-8")
    except FileNotFoundError:
        st.error(f"🚨 Video file not found at: {video_path}")
        return ""

def set_background_video(video_path):
    """Embed an MP4 video in Streamlit as a full-screen background."""
    video_base64 = video_to_base64(video_path)
    if video_base64:
        video_html = f"""
        <video autoplay loop muted playsinline style="
            position: fixed;
            right: 0;
            bottom: 0;
            min-width: 100vw;
            min-height: 100vh;
            object-fit: cover;
            z-index: -1;">
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>
        """
        st.markdown(video_html, unsafe_allow_html=True)

# ✅ Call function to set video background
if os.path.exists(VIDEO_PATH):
    set_background_video(VIDEO_PATH)
else:
    st.warning(f"⚠️ Background video not found at {VIDEO_PATH}. Please check the file path.")

# ✅ PREDICTION PAGE - Categorical Variables
APOE_CATEGORIES = ['APOE Genotype_2,2', 'APOE Genotype_2,3', 'APOE Genotype_2,4', 
                   'APOE Genotype_3,3', 'APOE Genotype_3,4', 'APOE Genotype_4,4']
PTHETHCAT_CATEGORIES = ['PTETHCAT_Hisp/Latino', 'PTETHCAT_Not Hisp/Latino', 'PTETHCAT_Unknown']
IMPUTED_CATEGORIES = ['imputed_genotype_True', 'imputed_genotype_False']
PTRACCAT_CATEGORIES = ['PTRACCAT_Asian', 'PTRACCAT_Black', 'PTRACCAT_White']
PTGENDER_CATEGORIES = ['PTGENDER_Female', 'PTGENDER_Male']
APOE4_CATEGORIES = ['APOE4_0', 'APOE4_1', 'APOE4_2']

ABBREVIATION = {
    "AD": "Alzheimer's Disease",
    "LMCI": "Late Mild Cognitive Impairment",
    "CN": "Cognitively Normal"
}

CONDITION_DESCRIPTION = {
    "AD": "This indicates that the individual's data aligns with characteristics commonly associated with "
          "Alzheimer's disease. Alzheimer's disease is a progressive neurodegenerative disorder that affects "
          "memory and cognitive functions.",
    "LMCI": "This suggests that the individual is in a stage of mild cognitive impairment that is progressing "
            "towards Alzheimer's disease. Mild Cognitive Impairment is a transitional state between normal "
            "cognitive aging and more significant cognitive decline.",
    "CN": "This suggests that the individual has normal cognitive functioning without significant impairments. "
          "This group serves as a control for comparison in Alzheimer's research."
}

# ✅ NEWS PAGE - Handle missing API key
NEWS_API_KEY = st.secrets.get("NEWS_API", None)
if not NEWS_API_KEY:
    st.warning("⚠️ Warning: NEWS_API key is missing in .streamlit/secrets.toml.")

KEYWORD = "alzheimer"

# ✅ CHATBOT PAGE - Handle missing secrets
HF_EMAIL = st.secrets.get("HF_GMAIL", None)
HF_PASS = st.secrets.get("HF_PASS", None)
BASE_PROMPT = st.secrets.get("BASE_PROMPT", "Analyze the user's symptoms and provide insights.")

if not HF_EMAIL or not HF_PASS:
    st.warning("⚠️ Warning: HF_GMAIL or HF_PASS is missing in .streamlit/secrets.toml.")
