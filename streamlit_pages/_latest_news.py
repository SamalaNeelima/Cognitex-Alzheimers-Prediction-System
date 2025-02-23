import html
import requests
import streamlit as st

# -------------------- CONFIGURATION -------------------- #

# Fetch API Key from secrets
API_KEY = st.secrets.get("NEWS_API", None)
KEYWORD = "Alzheimer"  # Replace with any relevant topic
DEFAULT_IMAGE = "https://via.placeholder.com/400?text=No+Image+Available"  # Placeholder for missing images

# Validate API Key
if not API_KEY:
    st.error("🚨 Error: NEWS_API key is missing in `.streamlit/secrets.toml`.")

# -------------------- FETCH NEWS FUNCTION -------------------- #

def _get_news():
    """Fetch news articles from NewsAPI with error handling."""
    if not API_KEY:
        st.error("⚠️ API key is missing! Please check your `.streamlit/secrets.toml` file.")
        return []

    try:
        response = requests.get(
            f'https://newsapi.org/v2/everything?q={KEYWORD}&apiKey={API_KEY}&language=en&searchIn=title'
        )
        data = response.json()

        # Handle API errors
        if response.status_code != 200:
            st.error(f"❌ API Error {response.status_code}: {data.get('message', 'Unknown error')}")
            return []

        return data.get('articles', [])
    
    except requests.RequestException as e:
        st.error(f"🌐 Network error: {e}")
        return []

# -------------------- DISPLAY NEWS FUNCTION -------------------- #

def news_page():
    """Render the news page with articles from NewsAPI."""
    st.title("📰 Latest News on Alzheimer’s")

    articles = _get_news()

    if not articles:
        st.warning("⚠️ No news articles found.")
        return

    for article in articles:
        # Extract article details with fallback values
        title = html.unescape(article.get('title', 'No Title'))
        description = html.unescape(article.get('description', 'No Description'))
        url = article.get('url', '#')
        urlToImage = article.get('urlToImage', None)
        author = article.get('author', 'Unknown')
        published_at = article.get('publishedAt', '')[:10]  # Extract only date (YYYY-MM-DD)

        # Use default image if the URL is missing
        if not urlToImage:
            urlToImage = DEFAULT_IMAGE

        # Display article with proper formatting
        st.subheader(title)
        st.image(urlToImage, use_container_width=True)  # ✅ Fixed deprecated parameter
        st.write(f"**{description}**")
        st.markdown(f"🔗 [Read more]({url})", unsafe_allow_html=True)
        st.caption(f"🖊️ Author: {author} | 📅 Published on: {published_at}")
        st.write("---")  # Divider between articles

# -------------------- HANDLE HUGGING FACE CREDENTIALS -------------------- #

HF_EMAIL = st.secrets.get("HF_GMAIL", None)
HF_PASS = st.secrets.get("HF_PASS", None)

if not HF_EMAIL:
    st.warning("⚠️ Warning: `HF_GMAIL` key is missing in `.streamlit/secrets.toml`.")

if not HF_PASS:
    st.warning("⚠️ Warning: `HF_PASS` key is missing in `.streamlit/secrets.toml`.")

# -------------------- RUN STREAMLIT APP -------------------- #

if __name__ == "__main__":
    news_page()
