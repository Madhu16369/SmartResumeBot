import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

nltk.download('punkt')

st.set_page_config(page_title="Smart AI Resume Guidance Bot", layout="centered")

st.title("🤖 Smart AI Resume Guidance Bot")
st.write("Create ATS-friendly and job-specific resumes")

name = st.text_input("Full Name")
job_role = st.selectbox("Target Job Role", [
    "Software Engineer", "Data Scientist", "Web Developer", "AI Engineer"
])

skills = st.text_area("Skills (comma separated)")
projects = st.text_area("Projects / Experience")
job_desc = st.text_area("Paste Job Description")

job_skill_map = {
    "software engineer": ["Python", "Java", "DSA", "OOPs", "Git"],
    "data scientist": ["Python", "Machine Learning", "SQL", "Statistics"],
    "web developer": ["HTML", "CSS", "JavaScript", "React"],
    "ai engineer": ["Python", "Deep Learning", "NLP"]
}

def calculate_ats_score(resume, jd):
    vector = CountVectorizer().fit_transform([resume, jd])
    return round(cosine_similarity(vector)[0][1] * 100, 2)

if st.button("Generate Resume"):
    suggested_skills = [
        skill for skill in job_skill_map[job_role.lower()]
        if skill.lower() not in skills.lower()
    ]

    resume_text = skills + projects
    ats_score = calculate_ats_score(resume_text, job_desc)

    st.subheader("🧠 Suggested Skills")
    st.write(suggested_skills)

    st.subheader("📊 ATS Match Score")
    st.success(f"{ats_score}%")

    doc = SimpleDocTemplate("resume.pdf")
    styles = getSampleStyleSheet()

    content = [
        Paragraph(f"<b>{name}</b>", styles["Title"]),
        Spacer(1, 10),
        Paragraph(f"Target Role: {job_role}", styles["Normal"]),
        Spacer(1, 10),
        Paragraph(f"<b>Skills:</b> {skills}", styles["Normal"]),
        Paragraph(f"<b>Projects:</b> {projects}", styles["Normal"]),
        Paragraph(f"<b>Suggested Skills:</b> {', '.join(suggested_skills)}", styles["Normal"]),
        Paragraph(f"<b>ATS Score:</b> {ats_score}%", styles["Normal"]),
    ]

    doc.build(content)

    st.download_button(
        "⬇️ Download Resume PDF",
        open("resume.pdf", "rb"),
        "Smart_Resume.pdf"
    )

