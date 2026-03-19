Austin News Reader 

## Application Preview

![](Placeholder.png)

Austin News Reader is an AI-powered web application designed to help users read and analyze news articles without distractions. The tool extracts the full article from a provided URL, formats it into readable paragraphs, generates an AI-powered summary, and allows users to download the article and summary as a PDF.

This project was built to simplify reading news articles related to policy, complaints, and oversight topics while eliminating paywall interruptions and clutter.

---

# Live Application

Streamlit App:  
https://shanthan-adblocker.streamlit.app/#enter-news-article-link
---

# Features

- Extract full news articles from any URL
- Automatically format articles into readable paragraphs
- Generate AI-powered article summaries
- Download article + AI summary as a PDF
- Display article source and metadata
- Clean and responsive user interface
- Social links and visitor counter
- Hosted publicly using Streamlit Cloud

---

# Project Architecture

User Flow:

1. User pastes a news article URL
2. The application extracts the article using `newspaper3k`
3. Article text is formatted into readable paragraphs
4. Users can generate an AI summary
5. Summary and full article can be downloaded as a PDF

---

# Technologies Used

## Programming Language

Python

---

## Web Application Framework

Streamlit

Used to build and deploy the interactive web application.

Key Components:

- st.title()
- st.markdown()
- st.button()
- st.download_button()
- st.session_state
- st.columns()

---

## AI Integration

OpenAI API

Model used:

gpt-4o-mini

Purpose:

- Generate bullet-point summaries of news articles

Library:

openai

---

## News Article Extraction

Library:

newspaper3k

Key Functions:

- Article(url)
- article.download()
- article.parse()

This library extracts:

- Article title
- Article text
- Clean content without ads

---

## PDF Generation

Library:

ReportLab

Key Components:

- SimpleDocTemplate
- Paragraph
- Spacer
- Stylesheets

Used to generate downloadable PDFs that contain:

- Article Title
- AI Summary
- Full Article
- Metadata (generated date + source URL)

---

## Text Processing

Python Libraries Used:

re (Regular Expressions)

Purpose:

- Clean whitespace
- Split article text into sentences
- Format paragraphs for readability

---

## Date and URL Parsing

Libraries:

datetime  
urllib.parse

Purpose:

- Add generation timestamp to PDF
- Extract article domain (source website)

Example:

Source URL: statesman.com

---

## UI Styling

Custom HTML and CSS were used within Streamlit to create a polished interface.

Features include:

- Austin skyline background with color overlay
- Custom button styling
- Social media icons
- Centered footer
- Visitor counter
- Logo placement

---

# Key Functions in the Project

## summarize_article()

Uses OpenAI to generate a bullet-point summary of the article.

Input:

Article text

Output:

AI-generated summary

---

## format_article_text()

Formats extracted article text into readable paragraphs.

Process:

1. Split article into sentences
2. Group sentences into paragraphs
3. Display paragraphs with proper spacing

---

## create_pdf()

Generates a downloadable PDF containing:

- Article title
- AI summary
- Full formatted article
- Metadata (date generated + source URL)

---

## get_base64_image()

Loads the Austin Police Oversight logo and embeds it in the web interface using Base64 encoding.

---

# Deployment

The application is hosted using Streamlit Cloud.

Deployment Steps:

1. Create a public GitHub repository
2. Push project code to GitHub
3. Add required dependencies in `requirements.txt`
4. Deploy via Streamlit Cloud
5. Connect repository to Streamlit app

Final hosted application:

[https://newsreader-8rj6jvdzimhasx54fzpiqr.streamlit.app/
](https://shanthan-adblocker.streamlit.app/#enter-news-article-link)
---

# Project Structure

news_reader  
│  
├── app.py  
├── requirements.txt  
├── README.md  
└── Austin-Police-Oversight-Logo-Faded-White.png  

---

# Example Workflow

User enters a news article URL:

https://www.statesman.com/news/article-example

The application will:

1. Extract article content
2. Format text into paragraphs
3. Generate AI summary
4. Allow PDF download of:
Article Title  
AI Summary  
Full Article  
Generated Date  
Source Website  

---

# Future Improvements

Possible enhancements for the application:

• Automatic monitoring of police-related news articles  
• Keyword highlighting for topics such as complaints or policy changes  
• Article sentiment analysis  
• Multi-article comparison  
• Database storage of analyzed articles  
• Dashboard for tracking trends in news coverage  

---

# Author

Shanthan Kasula

Portfolio  
https://shanthan-kasula-portfolio.netlify.app/

LinkedIn  
https://www.linkedin.com/in/shanthan-k/

GitHub  
https://github.com/shanthan98

---

# License
This project is intended for educational and research purposes.
