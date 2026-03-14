import streamlit as st
from newspaper import Article

st.title("📰 News Article Reader")

url = st.text_input("Paste the news article link")

if url:
    try:
        article = Article(url)
        article.download()
        article.parse()

        st.header(article.title)
        st.write(article.text)

    except:
        st.error("Could not extract article content.")