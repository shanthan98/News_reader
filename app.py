from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
import io
import streamlit as st
from newspaper import Article
import base64
from openai import OpenAI
if "article_text" not in st.session_state:
    st.session_state.article_text = None

if "article_title" not in st.session_state:
    st.session_state.article_title = None
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def summarize_article(text):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize news articles in clear bullet points."
            },
            {
                "role": "user",
                "content": text[:4000]
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
def create_pdf(title, summary, article_text):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []

    # Title
    story.append(Paragraph(f"<b>{title}</b>", styles["Title"]))
    story.append(Spacer(1, 20))

    # Summary
    story.append(Paragraph("<b>AI Summary</b>", styles["Heading2"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(summary.replace("\n", "<br/>"), styles["BodyText"]))
    story.append(Spacer(1, 20))

    # Article
    story.append(Paragraph("<b>Full Article</b>", styles["Heading2"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(article_text.replace("\n", "<br/>"), styles["BodyText"]))

    doc.build(story)

    buffer.seek(0)
    return buffer

# Function must be defined first
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Now call the function
logo_base64 = get_base64_image("Austin-Police-Oversight-Logo-Faded-White.png")

st.set_page_config(
    page_title="Austin News Reader",
    page_icon="",
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
st.markdown(
    """
    <style>

    /* Fix button visibility */
    div.stButton > button {
        background-color: #44499C;
        color: white;
        border-radius: 6px;
        border: none;
        height: 38px;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background-color: #2f347a;
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("""
<style>

/* Center the search container */
.search-container {
    max-width: 800px;
    margin: auto;
}

/* Style the input field */
div[data-baseweb="input"] input {
    border-radius: 30px;
    height: 46px;
    padding-left: 18px;
    font-size: 16px;
}

/* Style the button */
div.stButton > button {
    background-color: #44499C;
    color: white;
    border-radius: 30px;
    height: 46px;
    font-weight: 600;
    border: none;
}

div.stButton > button:hover {
    background-color: #2f347a;
}

</style>
""", unsafe_allow_html=True)

st.title("APO News Reader")
st.markdown("Paste a news article link below to read it without ads or subscription popups.")

st.markdown("---")

st.subheader("🔗 Enter News Article Link")

st.markdown('<div class="search-container">', unsafe_allow_html=True)

col1, col2 = st.columns([8,2])

with col1:
    url = st.text_input(
        "",
        placeholder="Paste a news article URL...",
        label_visibility="collapsed"
    )

with col2:
    submit = st.button("🔎 Read Article", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

if submit and url:
    try:
        with st.spinner("Fetching article..."):
            article = Article(url)
            article.download()
            article.parse()

        st.session_state.article_text = article.text
        st.session_state.article_title = article.title

        st.success("Article loaded successfully!")

    except Exception:
        st.error("❌ Could not extract article content.")
if st.session_state.article_text:

    st.subheader(st.session_state.article_title)

    st.markdown("### Article Content")
    st.write(st.session_state.article_text)

    st.markdown("---")

    if st.button("🤖 Generate AI Summary", type="primary"):

    with st.spinner("Generating AI summary..."):
        st.session_state.summary = summarize_article(st.session_state.article_text)

if st.session_state.summary:

    st.markdown("## 🤖 AI Summary")
    st.write(st.session_state.summary)
if "summary" not in st.session_state:
    st.session_state.summary = None
if st.session_state.summary:

    pdf_file = create_pdf(
        st.session_state.article_title,
        st.session_state.summary,
        st.session_state.article_text
    )

    st.download_button(
        label="📄 Download Article + Summary as PDF",
        data=pdf_file,
        file_name="article_summary.pdf",
        mime="application/pdf"
    )
