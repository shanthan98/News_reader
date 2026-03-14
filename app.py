import streamlit as st
from newspaper import Article
import base64

# Function must be defined first
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Now call the function
logo_base64 = get_base64_image("Austin-Police-Oversight-Logo-Faded-White.png")

st.set_page_config(
    page_title="Austin News Reader",
    page_icon="📰",
    layout="wide"
)
# Background styling
st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            rgba(68, 73, 156, 0.85),
            rgba(68, 73, 156, 0.85)
        ),
        url("https://images.unsplash.com/photo-1531218150217-54595bc2b934");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    h1, h2, h3, h4, h5, h6, p, div, label, span {
        color: white !important;
    }

    input {
        background-color: white !important;
        color: black !important;
        border-radius: 6px;
    }

    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    f"""
    <style>
    .logo-container {{
        position: fixed;
        top: 70px;
        right: 30px;
        z-index: 1000;
    }}

    .logo-container img {{
        width: 140px;
        opacity: 0.95;
    }}
    </style>

    <div class="logo-container">
        <img src="data:image/png;base64,{logo_base64}">
    </div>
    """,
    unsafe_allow_html=True
)
st.title("📰 APO News Reader")
st.markdown("Paste a news article link below to read it without ads or subscription popups.")

st.markdown("---")

st.subheader("🔗 Enter News Article Link")

url = st.text_input(
    "Paste the article URL here:",
    placeholder="https://www.statesman.com/..."
)

st.markdown("---")

if url:
    try:
        with st.spinner("Fetching article..."):
            article = Article(url)
            article.download()
            article.parse()

        st.success("Article loaded successfully!")

        st.subheader(article.title)

        st.markdown("### Article Content")
        st.write(article.text)

    except:
        st.error("❌ Could not extract article content.")
