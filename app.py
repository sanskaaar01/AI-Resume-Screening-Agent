import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import re

# =====================================================
# OPENROUTER CONFIG
# =====================================================

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_OPENROUTER_API_KEY"
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Resume Screening Agent",
    page_icon="🤖",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #0f172a;
    color: white;
}

h1, h2, h3 {
    color: white;
}

.stTextArea textarea {
    background-color: #1e293b;
    color: white;
}

.report-box {
    padding: 20px;
    border-radius: 12px;
    background-color: #1e293b;
    margin-top: 20px;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.title("🤖 AI Resume Screening Agent")

st.write(
    "Analyze resumes against job descriptions using AI-powered ATS screening and hiring intelligence."
)

# =====================================================
# PDF TEXT EXTRACTION
# =====================================================

def extract_text_from_pdf(uploaded_file):

    pdf_reader = PdfReader(uploaded_file)

    text = ""

    for page in pdf_reader.pages:

        extracted_text = page.extract_text()

        if extracted_text:
            text += extracted_text

    return text

# =====================================================
# LAYOUT
# =====================================================

col1, col2 = st.columns(2)

# =====================================================
# LEFT COLUMN
# =====================================================

with col1:

    st.subheader("📄 Upload Resume")

    uploaded_file = st.file_uploader(
        "Choose Resume PDF",
        type=["pdf"]
    )

    st.subheader("📝 Job Description")

    job_description = st.text_area(
        "Paste Job Description Here",
        height=300
    )

    analyze_button = st.button("🚀 Analyze Resume")

# =====================================================
# RIGHT COLUMN
# =====================================================

with col2:

    st.subheader("📊 AI Screening Report")

    if analyze_button:

        if uploaded_file is None:
            st.error("Please upload a resume PDF.")

        elif job_description.strip() == "":
            st.error("Please paste a job description.")

        else:

            with st.spinner("AI is analyzing the resume..."):

                # Extract Resume Text
                resume_text = extract_text_from_pdf(uploaded_file)

                # =====================================================
                # PROMPT
                # =====================================================

                prompt = f"""
You are an advanced AI Resume Screening Agent.

Analyze the candidate resume against the provided job description.

========================
RESUME
========================

{resume_text}

========================
JOB DESCRIPTION
========================

{job_description}

Provide a professional hiring report with the following sections:

1. Candidate Summary
2. Matching Technical Skills
3. Missing Technical Skills
4. Project Relevance
5. ATS Match Score (out of 100)
6. Key Strengths
7. Areas for Improvement
8. Final Hiring Recommendation

For Final Hiring Recommendation choose ONLY one:
- Strong Fit
- Moderate Fit
- Weak Fit

Keep the response concise, structured, professional, and recruiter-oriented.
"""

                try:

                    # =====================================================
                    # API CALL
                    # =====================================================

                    completion = client.chat.completions.create(
                        model="openai/gpt-3.5-turbo",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )

                    result = completion.choices[0].message.content

                    # =====================================================
                    # ATS SCORE EXTRACTION
                    # =====================================================

                    score_match = re.search(r'(\d{1,3})/100', result)

                    if score_match:

                        score = int(score_match.group(1))

                        st.metric(
                            label="ATS Match Score",
                            value=f"{score}%"
                        )

                    # =====================================================
                    # HIRING DECISION
                    # =====================================================

                    if "Strong Fit" in result:
                        st.success("🟢 Hiring Decision: STRONG FIT")

                    elif "Moderate Fit" in result:
                        st.warning("🟡 Hiring Decision: MODERATE FIT")

                    elif "Weak Fit" in result:
                        st.error("🔴 Hiring Decision: WEAK FIT")

                    # =====================================================
                    # SUCCESS MESSAGE
                    # =====================================================

                    st.success("✅ Analysis Completed Successfully")

                    # =====================================================
                    # DISPLAY RESULT
                    # =====================================================

                    st.markdown(
                        f"""
                        <div class="report-box">
                        {result}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # =====================================================
                    # DOWNLOAD BUTTON
                    # =====================================================

                    st.download_button(
                        label="📥 Download Report",
                        data=result,
                        file_name="resume_analysis_report.txt",
                        mime="text/plain"
                    )

                except Exception as e:

                    st.error(f"Error: {e}")

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption("Built using Streamlit + OpenRouter API")