# ----------- IMPORT REQUIRED LIBRARIES -----------

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
import io
import re
from datetime import datetime
from urllib.parse import urlparse


import streamlit as st
from newspaper import Article
import base64
from openai import OpenAI


# ----------- INITIALIZE SESSION STATE VARIABLES -----------

if "article_text" not in st.session_state:
    st.session_state.article_text = None

if "article_title" not in st.session_state:
    st.session_state.article_title = None

if "summary" not in st.session_state:
    st.session_state.summary = None


# ----------- INITIALIZE OPENAI CLIENT -----------

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# ----------- FUNCTION: GENERATE AI SUMMARY -----------

def summarize_article(text):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "Summarize news articles in clear bullet points."},
            {"role": "user",
             "content": text[:4000]}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
    
# ----------- FUNCTION: Fallback Code -----------
    
def fallback_extract(url):
    import requests
    from bs4 import BeautifulSoup

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text(strip=True) for p in paragraphs])

        # ❗ Remove garbage / JS-block content
        if "JavaScript is disabled" in text or len(text) < 300:
            return ""

        return text

    except:
        return ""
 # ----------- FUNCTION: Helper Function-----------
       
def get_amp_url(url):
    if url.endswith(".php"):
        return url.replace(".php", ".php?outputType=amp")
    return url + "?outputType=amp"
    
# ----------- FUNCTION: FORMAT ARTICLE INTO PARAGRAPHS -----------

def format_article_text(text, sentences_per_paragraph=4):

    # Clean extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    paragraphs = []
    current = []

    for sentence in sentences:
        current.append(sentence)

        if len(current) >= sentences_per_paragraph:
            paragraphs.append(" ".join(current))
            current = []

    if current:
        paragraphs.append(" ".join(current))

    return paragraphs

# ----------- FUNCTION: CREATE PDF FILE -----------

def create_pdf(title, summary, article_text, source_url):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []

    # Article title
    story.append(Paragraph(f"<b>{title}</b>", styles["Title"]))
    story.append(Spacer(1, 20))

    # AI summary section
    story.append(Paragraph("<b>AI Summary</b>", styles["Heading2"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(summary.replace("\n", "<br/>"), styles["BodyText"]))
    story.append(Spacer(1, 20))

    # Full article section
    story.append(Paragraph("<b>Full Article</b>", styles["Heading2"]))
    story.append(Spacer(1, 10))

    formatted_paragraphs = format_article_text(article_text)

    for para in formatted_paragraphs:
        story.append(Paragraph(para, styles["BodyText"]))
        story.append(Spacer(1, 12))

    # -------- Footer metadata --------

    story.append(Spacer(1, 30))

    generated_date = datetime.now().strftime("%B %d, %Y")
    domain = urlparse(source_url).netloc

    story.append(Paragraph(f"<i>Generated: {generated_date}</i>", styles["BodyText"]))
    story.append(Paragraph(f"<i>Source URL: {domain}</i>", styles["BodyText"]))

    doc.build(story)

    buffer.seek(0)
    return buffer


# ----------- FUNCTION: LOAD LOGO IMAGE -----------

def get_base64_image(image_path):

    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


logo_base64 = get_base64_image("Austin-Police-Oversight-Logo-Faded-White.png")


# ----------- PAGE CONFIGURATION -----------

st.set_page_config(
    page_title="Austin News Reader",
    page_icon="",
    layout="wide"
)


# ----------- BACKGROUND + GLOBAL STYLING -----------

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            rgba(68,73,156,0.85),
            rgba(68,73,156,0.85)
        ),
        url("https://images.unsplash.com/photo-1531218150217-54595bc2b934");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    h1,h2,h3,h4,h5,h6,p,div,label,span {
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


# ----------- DISPLAY LOGO TOP RIGHT -----------

st.markdown(
    f"""
    <style>
    .logo-container {{
        position: fixed;
        top: 70px;
        right: 20px;
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


# ----------- BUTTON STYLING -----------

st.markdown("""
<style>

/* Style BOTH normal buttons and download buttons */
div.stButton > button,
div.stDownloadButton > button {

    background-color: #44499C;
    color: white;
    border-radius: 30px;
    height: 46px;
    padding: 0px 22px;
    font-weight: 600;
    border: none;
    width: auto;
}

/* Hover effect */
div.stButton > button:hover,
div.stDownloadButton > button:hover {
    background-color: #2f347a;
}

</style>
""", unsafe_allow_html=True)


# ----------- PAGE TITLE -----------

st.title("Austin News Reader")
st.markdown("Paste a news article link below to read it without ads or subscription popups.")
st.markdown("---")


# ----------- URL INPUT SEARCH BAR -----------

st.subheader("🔗 Enter News Article Link")

col1, col2 = st.columns([8,2])

with col1:
    url = st.text_input(
        "",
        placeholder="Paste a news article URL...",
        label_visibility="collapsed"
    )

with col2:
    submit = st.button("Read Article", use_container_width=True)

st.markdown("---")


# ----------- FETCH ARTICLE WHEN USER CLICKS READ -----------

with st.spinner("Fetching article..."):

    text = ""
    title = ""

    # -------- Attempt 1: Newspaper --------
    try:
        article = Article(url)
        article.download()
        article.parse()

        text = article.text
        title = article.title

        if text and len(text) > 300:
            st.success("Article extracted using standard method.")

        else:
            raise Exception("Weak content")

    except Exception:

        st.warning("Standard extraction failed. Trying AMP version...")

        # -------- Attempt 2: AMP --------
        try:
            amp_url = get_amp_url(url)

            amp_article = Article(amp_url)
            amp_article.download()
            amp_article.parse()

            text = amp_article.text
            title = amp_article.title

            if text and len(text) > 300:
                st.success("Article extracted using AMP version.")
            else:
                raise Exception("AMP failed")

        except Exception:

            st.warning("AMP failed. Using fallback extraction...")

            # -------- Attempt 3: BeautifulSoup --------
            text = fallback_extract(url)
            title = "Untitled Article"

    # -------- Final assignment --------
    st.session_state.article_text = text
    st.session_state.article_title = title
    st.session_state.summary = None
    
    if not text or "JavaScript is disabled" in text or len(text) < 300:
        st.error("Unable to extract article content from this website.")
        st.info("Try opening the article in browser reader mode or use another link.")
        st.stop()

# ----------- DISPLAY ARTICLE CONTENT -----------

if st.session_state.article_text:

    st.subheader(st.session_state.article_title)

    st.markdown("### Article Content")

    formatted_paragraphs = format_article_text(st.session_state.article_text)

    for para in formatted_paragraphs:
        st.markdown(f"<p style='margin-bottom:18px; line-height:1.6'>{para}</p>", unsafe_allow_html=True)

    st.markdown("---")

    if st.button("Generate AI Summary", type="primary"):

        with st.spinner("Generating AI summary..."):
            st.session_state.summary = summarize_article(st.session_state.article_text)


# ----------- DISPLAY SUMMARY -----------

if st.session_state.summary:

    st.markdown("## 🤖 AI Summary")
    st.write(st.session_state.summary)

    # ----------- DOWNLOAD PDF BUTTON -----------

    pdf_file = create_pdf(
        st.session_state.article_title,
        st.session_state.summary,
        st.session_state.article_text,
        url
    )

    st.download_button(
        label="Download as PDF",
        data=pdf_file,
        file_name="article_summary.pdf",
        mime="application/pdf"
    )
    
# =====================================================
# FOOTER SECTION
# =====================================================

st.markdown("---")


# -----------------------------------------------------
# FOOTER STYLING
# Makes sure footer container has no white background
# and centers everything nicely
# -----------------------------------------------------

st.markdown("""
<style>

.footer-container {
    text-align: center;
    margin-top: 50px;
    padding-bottom: 40px;
}

/* Social icon row */
.footer-icons {
    display: flex;
    justify-content: center;
    gap: 30px;
    margin-top: 15px;
    margin-bottom: 35px;
}

/* Visitor section */
.visitor-title {
    font-size: 20px;
    text-decoration: underline;
    margin-bottom: 10px;
}

/* Copyright text */
.footer-copy {
    font-size: 14px;
    opacity: 0.9;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)


# ----------- FOOTER SECTION -----------

st.markdown("---")

st.markdown(
"""
<div style="text-align:center; margin-top:30px;">

<p style="font-size:18px; margin-bottom:10px;">Find me on</p>

<div style="display:flex; justify-content:center; gap:30px; margin-bottom:20px;">

<a href="https://github.com/shanthan98" target="_blank">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" width="32">
</a>

<a href="https://www.linkedin.com/in/shanthan-k/" target="_blank">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" width="32">
</a>

<a href="https://shanthan-kasula-portfolio.netlify.app/" target="_blank">
<img src="https://cdn-icons-png.flaticon.com/512/1006/1006771.png" width="32">
</a>

</div>

<div style="margin-bottom:15px;">
<img src="https://hitwebcounter.com/counter/counter.php?page=21484222&style=0011&nbdigits=5&type=page&initCount=67"/>
</div>

<p style="font-size:14px;">
Copyright ©2026 All rights reserved | This template is made by Shanthan


</p>

</div>
""",
unsafe_allow_html=True
)
