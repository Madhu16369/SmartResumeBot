import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Smart AI Resume Guidance Bot",
    page_icon="📄",
    layout="wide"
)

# -------------------- SIDEBAR --------------------
st.sidebar.title("📌 Smart Resume Bot")
menu = st.sidebar.radio(
    "Navigation",
    ["Resume Builder", "ATS Score", "AI Skill Suggestions"]
)

# -------------------- JOB ROLE SKILL MAP --------------------
job_skill_map = {
    "software engineer": ["Python", "Java", "DSA", "OOPs", "Git", "SQL"],
    "data scientist": ["Python", "Machine Learning", "SQL", "Statistics", "Pandas"],
    "web developer": ["HTML", "CSS", "JavaScript", "React", "Bootstrap"],
    "ai engineer": ["Python", "Deep Learning", "NLP", "TensorFlow", "PyTorch"]
}

# -------------------- FUNCTIONS --------------------
def improve_grammar(text):
    """
    Cloud-safe grammar improvement function.
    Uses NLTK if available, otherwise falls back to basic sentence splitting.
    """
    if not text:
        return ""

    try:
        sentences = nltk.sent_tokenize(text)
    except LookupError:
        sentences = text.split(".")

    improved_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            improved_sentences.append(sentence.capitalize())

    return ". ".join(improved_sentences)

def calculate_ats_score(resume_text, job_description):
    if not resume_text or not job_description:
        return 0.0

    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_description])
    score = cosine_similarity(vectors)[0][1]
    return round(score * 100, 2)

def generate_pdf(name, job_role, skills, projects, suggestions, ats_score):
    doc = SimpleDocTemplate("resume.pdf")
    styles = getSampleStyleSheet()

    content = [
        Paragraph(f"<b>{name}</b>", styles["Title"]),
        Spacer(1, 12),
        Paragraph(f"<b>Target Role:</b> {job_role}", styles["Normal"]),
        Spacer(1, 12),
        Paragraph(f"<b>Skills:</b> {skills}", styles["Normal"]),
        Spacer(1, 10),
        Paragraph(f"<b>Projects / Experience:</b> {projects}", styles["Normal"]),
        Spacer(1, 10),
        Paragraph(f"<b>AI Suggested Skills:</b> {', '.join(suggestions)}", styles["Normal"]),
        Spacer(1, 10),
        Paragraph(f"<b>ATS Match Score:</b> {ats_score}%", styles["Normal"]),
    ]

    doc.build(content)

# -------------------- RESUME BUILDER --------------------
if menu == "Resume Builder":
    st.title("📄 Resume Builder")

    name = st.text_input("Full Name")
    job_role = st.selectbox(
        "Target Job Role",
        ["Software Engineer", "Data Scientist", "Web Developer", "AI Engineer"]
    )

    skills = st.text_area("Your Skills (comma separated)")
    project_input = st.text_area("Projects / Experience")
    projects = improve_grammar(project_input)

    job_description = st.text_area("Paste Job Description")

    if st.button("🚀 Generate Resume"):
        role_key = job_role.lower()

        suggested_skills = [
            skill for skill in job_skill_map[role_key]
            if skill.lower() not in skills.lower()
        ]

        resume_text = f"{skills} {projects}"
        ats_score = calculate_ats_score(resume_text, job_description)

        st.success("Resume Generated Successfully!")

        st.subheader("🧠 AI Skill Suggestions")
        if suggested_skills:
            for skill in suggested_skills:
                st.write("✔️", skill)
        else:
            st.write("Your skills already match the role well 👍")

        st.subheader("📊 ATS Resume Score")
        st.metric("ATS Compatibility", f"{ats_score}%")

        generate_pdf(
            name, job_role, skills, projects, suggested_skills, ats_score
        )

        st.download_button(
            "⬇️ Download Resume PDF",
            open("resume.pdf", "rb"),
            "Smart_AI_Resume.pdf"
        )

# -------------------- ATS SCORE PAGE --------------------
elif menu == "ATS Score":
    st.title("📊 ATS Resume Score Checker")

    resume_text = st.text_area("Paste Your Resume Text")
    job_description = st.text_area("Paste Job Description")

    if st.button("Check ATS Score"):
        score = calculate_ats_score(resume_text, job_description)
        st.metric("ATS Match Percentage", f"{score}%")

# -------------------- AI SKILL SUGGESTIONS --------------------
elif menu == "AI Skill Suggestions":
    st.title("🤖 AI Skill Recommendation")

    job_role = st.selectbox(
        "Select Job Role",
        ["Software Engineer", "Data Scientist", "Web Developer", "AI Engineer"]
    )

    current_skills = st.text_area("Enter Your Current Skills")

    if st.button("Get Skill Suggestions"):
        role_key = job_role.lower()

        missing_skills = [
            skill for skill in job_skill_map[role_key]
            if skill.lower() not in current_skills.lower()
        ]

        st.subheader("📌 Recommended Skills")
        if missing_skills:
            for skill in missing_skills:
                st.write("✔️", skill)
        else:
            st.write("Your skill set is well aligned with this role 🎯")

