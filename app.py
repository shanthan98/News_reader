import streamlit as st
from newspaper import Article

st.set_page_config(
    page_title="Austin News Reader",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Austin News Reader")
st.markdown("Paste a news article link below to read it without ads or subscription popups.")

st.markdown("---")

# Clear input section
st.subheader("🔗 Enter News Article Link")

url = st.text_input(
    label="Paste the article URL here:",
    placeholder="https://www.statesman.com/...",
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
