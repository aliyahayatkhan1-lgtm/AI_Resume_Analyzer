import streamlit as st
import pdfplumber
import pandas as pd

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# Skill Database
# -----------------------------
SKILLS = [
    "python", "java", "c++", "sql",
    "machine learning", "deep learning",
    "artificial intelligence", "nlp",
    "data science", "tensorflow",
    "pytorch", "streamlit",
    "html", "css", "javascript",
    "react", "git", "github",
    "excel", "power bi"
]

# -----------------------------
# Extract Text From PDF
# -----------------------------
def extract_text(pdf_file):
    text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + " "

    return text.lower()

# -----------------------------
# Skill Matching
# -----------------------------
def find_skills(text):
    found = []

    for skill in SKILLS:
        if skill in text:
            found.append(skill)

    return found

# -----------------------------
# Resume Scoring
# -----------------------------
def calculate_score(skills):
    score = min(len(skills) * 5, 100)
    return score

# -----------------------------
# Suggestions
# -----------------------------
def suggestions(score):

    tips = []

    if score < 30:
        tips.append("Add more technical skills.")
        tips.append("Include projects section.")
        tips.append("Mention internships and certifications.")

    elif score < 60:
        tips.append("Add measurable achievements.")
        tips.append("Improve project descriptions.")
        tips.append("Include GitHub and LinkedIn links.")

    else:
        tips.append("Strong resume profile.")
        tips.append("Keep updating projects.")
        tips.append("Tailor resume for each job.")

    return tips

# -----------------------------
# UI
# -----------------------------
st.title("🤖 AI Resume Analyzer")
st.markdown("Upload your resume and get instant AI analysis.")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:

    text = extract_text(uploaded_file)

    skills_found = find_skills(text)

    score = calculate_score(skills_found)

    st.success("Resume analyzed successfully!")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Resume Score")

        st.progress(score / 100)

        st.metric(
            "Score",
            f"{score}/100"
        )

    with col2:
        st.subheader("Skills Found")

        if skills_found:
            for skill in skills_found:
                st.write("✅", skill.title())
        else:
            st.warning("No skills detected.")

    st.subheader("Improvement Suggestions")

    for tip in suggestions(score):
        st.write("📌", tip)

    st.subheader("Resume Summary")

    st.write(
        f"""
        Total Skills Detected: {len(skills_found)}

        Resume Strength: {"Excellent" if score >= 70 else "Average" if score >= 40 else "Needs Improvement"}
        """
    )

    st.subheader("Detected Resume Text")

    st.text_area(
        "",
        text[:3000],
        height=300
    )