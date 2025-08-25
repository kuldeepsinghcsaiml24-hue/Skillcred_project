import streamlit as st
import google.generativeai as genai
import os
from PyPDF2 import PdfReader
from docx import Document

# -------------------------------
# 🔑 Configure Gemini API
# -------------------------------
genai.configure(api_key="AIzaSyA7sIoU-9mHvzdvcKcVaXSgrQlTntSkRPs")

# -------------------------------
# 📂 Helper functions
# -------------------------------
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def generate_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text if response and response.text else "⚠️ No response from Gemini."

# -------------------------------
# 🌐 Streamlit App
# -------------------------------
st.set_page_config(
    page_title="AI Resume Generator",
    page_icon="🚀",
    layout="wide"
)

# ✅ Background Image + Glassmorphism
st.markdown("""
    <style>
        .stApp {
            background-image: url("https://wallpapercave.com/wp/wp11404483.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        .glass-box {
            background: rgba(255, 255, 255, 0.75);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# UI
# -------------------------------
st.title("🚀 AI Resume & Cover Letter Generator")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.subheader("📂 Upload Resume / LinkedIn Profile")

    uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
    linkedin_text = st.text_area("Or paste your LinkedIn profile summary", height=120)

    job_description = st.text_area("📝 Paste Job Description", height=180)

    tone = st.selectbox("Select Tone", ["Professional", "Direct", "Enthusiastic"])

    generate_button = st.button("🚀 Generate")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.subheader("📄 Generated Results")
    results_placeholder = st.empty()
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# 🔄 Main Processing
# -------------------------------
if generate_button:
    if not uploaded_file and not linkedin_text:
        st.error("⚠️ Please upload a resume or paste LinkedIn text.")
    elif not job_description:
        st.error("⚠️ Please paste the job description.")
    else:
        with st.spinner("⚙️ Generating tailored Resume & Cover Letter..."):
            resume_text = ""

            if uploaded_file:
                if uploaded_file.type == "application/pdf":
                    resume_text = extract_text_from_pdf(uploaded_file)
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    resume_text = extract_text_from_docx(uploaded_file)

            if linkedin_text and not resume_text:
                resume_text = linkedin_text

            # STRICT PROMPT
            prompt = f"""
You are an expert AI resume writer.
The user has provided this resume content:
{resume_text}

And this job description:
{job_description}

Write the output ONLY in the following exact structure:

📄 Tailored Resume Format

[Full Name]
[Email] | [Phone] | [LinkedIn] | [Portfolio/GitHub]

Professional Summary
2–3 sentences tailored to the job description, highlighting most relevant skills, achievements, and career goals.

Skills
- [Skill 1]
- [Skill 2]
- [Skill 3]
- [Skill 4]

Experience
[Role] – [Company/Organization] (YYYY–YYYY)
• Achievement/responsibility relevant to JD.
• Achievement/responsibility with measurable impact.
• Tech/tools used.

Education
[Degree, Field] – [University/Institute] (YYYY–YYYY)
Relevant coursework/projects if applicable.

Projects (Optional)
[Project Title] – Short 1–2 line description highlighting impact/tech used.

📧 Cover Letter Format

[Your Name]
[City, Country]
[Email] | [Phone]

Date: [DD Month YYYY]

Hiring Manager
[Company Name]
[Location]

Subject: Application for [Job Title/Internship]

Paragraph 1 – Introduction
Paragraph 2 – Why You Fit
Paragraph 3 – Why Them
Paragraph 4 – Closing

Sincerely,
[Your Name]
use this format for basic and standard but while writing the output remove the headings like this Paragraph 1 – Introduction
Paragraph 2 – Why You Fit
Paragraph 3 – Why Them
Paragraph 4 – Closing
and put the information you get from linked profile 
use the other fomat if needed and the user refresh and want another response 

Use a {tone} tone. Do not include any text outside this format.
"""

            result_text = generate_with_gemini(prompt)

            results_placeholder.markdown("**✅ Generated successfully!**")

            st.markdown("### 📝 Tailored Resume + Cover Letter")
            st.text_area("Output", result_text, height=600)
