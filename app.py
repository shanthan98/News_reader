import streamlit as st
from newspaper import Article

st.set_page_config(
    page_title="Austin News Reader",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Austin News Reader")
st.markdown("Paste a news article link below to read it without ads or subscription popups.")

url = st.text_input("🔗 Paste Article URL")

if url:
    try:
        article = Article(url)
        article.download()
        article.parse()

        st.subheader(article.title)

        st.markdown("### Article Content")
        st.write(article.text)

    except:
        st.error("❌ Could not extract article content.")
