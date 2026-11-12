
import plotly.graph_objects as go
import streamlit as st
import pymupdf
import re
import html


# Page settings
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# Professional background and styling
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at 15% 10%,
            rgba(88, 80, 220, 0.30), transparent 35%),
        radial-gradient(ellipse at 85% 70%,
            rgba(0, 180, 220, 0.18), transparent 40%),
        linear-gradient(135deg, #070b1a, #111b38, #091326);
    background-attachment: fixed;
    color: #f0f4ff;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #f0f4ff !important;
}

.hero {
    text-align: center;
    padding: 38px 20px;
    border: 1px solid rgba(150, 160, 255, 0.25);
    border-radius: 22px;
    background: rgba(30, 40, 80, 0.45);
    margin-bottom: 30px;
}

.hero h1 {
    font-size: 46px;
    font-weight: 800;
    background: linear-gradient(90deg, #77d9ff, #bd91ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #c1cbe2;
    font-size: 17px;
}

[data-testid="stMetric"] {
    background: rgba(35, 48, 91, 0.8);
    border: 1px solid rgba(135, 155, 255, 0.25);
    border-radius: 16px;
    padding: 22px;
}

[data-testid="stMetricValue"] {
    color: #80dcff;
}

.stButton > button {
    background: linear-gradient(90deg, #6258e8, #267bcf);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 30px;
    font-weight: 700;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #746aff, #3498ee);
    color: white;
    border: none;
}

[data-testid="stFileUploader"],
[data-testid="stTextArea"] {
    border-radius: 12px;
}

.footer {
    text-align: center;
    color: #98a7c5;
    padding: 35px 10px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


# Recognized skills
skills = [
    "Python", "SQL", "Excel", "Pandas",
    "Power BI", "Tableau", "Machine Learning",
    "Java", "HTML", "CSS", "JavaScript",
    "Data Visualization", "Statistics",
    "NumPy", "Scikit-learn", "TensorFlow",
    "Git", "GitHub", "MongoDB", "AWS",
    "Data Analysis", "Deep Learning",
    "NLP", "Streamlit"
]


# Read uploaded PDF
def readresume(resume):
    text = ""

    with pymupdf.open(
        stream=resume.getvalue(),
        filetype="pdf"
    ) as pdf:
        for page in pdf:
            text += page.get_text()

    return text


# Identify skills in text
def findskills(text):
    found = []

    for skill in skills:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text, re.IGNORECASE):
            found.append(skill)

    return found


# Application heading
st.markdown("""
<div class="hero">
    <h1>🚀 AI Resume Analyzer</h1>
    <p>Discover your strengths. Identify skill gaps.
    Improve your resume.</p>
    <p>Smart Resume Analysis Dashboard</p>
</div>
""", unsafe_allow_html=True)


# Upload section
st.subheader("📂 Upload Resume & Job Description")

col1, col2 = st.columns(2, gap="large")

with col1:
    resume = st.file_uploader(
        "Upload your resume (PDF)",
        type=["pdf"]
    )

with col2:
    job = st.text_area(
        "Paste the Job Description",
        height=180,
        placeholder="Paste the job requirements here..."
    )

st.write("")

analyze = st.button(
    "🔍 Analyze My Resume",
    use_container_width=True
)


# Resume analysis
if analyze:

    if resume is None or not job.strip():
        st.warning(
            "Please upload a PDF resume and enter a job description."
        )

    else:
        try:
            text = readresume(resume)

        except Exception:
            st.error(
                "Unable to read this PDF. Please try another file."
            )
            st.stop()

        if not text.strip():
            st.warning(
                "No readable text found. Please use a text-based PDF."
            )

        else:
            st.success("Resume analyzed successfully!")

            resumekills = findskills(text)
            jobskills = findskills(job)

            matching = [
                skill for skill in jobskills
                if skill in resumekills
            ]

            missing = [
                skill for skill in jobskills
                if skill not in resumekills
            ]

            if jobskills:

                score = len(matching) / len(jobskills) * 100

                # Dashboard
                st.markdown("---")
                st.header("📊 Resume Analysis Dashboard")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "🎯 Skill Match",
                        f"{score:.1f}%"
                    )

                with col2:
                    st.metric(
                        "✅ Matching Skills",
                        len(matching)
                    )

                with col3:
                    st.metric(
                        "📌 Missing Skills",
                        len(missing)
                    )

                st.write("### Overall Skill Match")
                st.progress(int(score))

                # Skill Match Doughnut Chart
                st.subheader("📊 Skill Match Visualization")

                fig = go.Figure(
                    data=[
                        go.Pie(
                            labels=["Matching Skills", "Missing Skills"],
                            values=[len(matching), len(missing)],
                            hole=0.6,
                            marker=dict(
                                colors=["#35d6b0", "#ff8a80"]
                            ),
                            textinfo="label+percent"
                        )
                    ]
                )

                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=350,
                    annotations=[
                        dict(
                            text=f"{score:.0f}%",
                            x=0.5,
                            y=0.5,
                            showarrow=False,
                            font_size=30
                        )
                    ]
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


                st.caption(
                    "Percentage of recognized job skills "
                    "detected in the resume. "
                    "This is not an official ATS score."
                )

                # Matching and missing skills
                st.markdown("---")

                left, right = st.columns(2, gap="large")

                with left:
                    st.subheader("✅ Matching Skills")

                    if matching:
                        for skill in matching:
                            st.success(skill)
                    else:
                        st.info("No matching skills detected.")

                with right:
                    st.subheader("📌 Missing Skills")

                    if missing:
                        for skill in missing:
                            st.warning(skill)
                    else:
                        st.success(
                            "All recognized job skills detected!"
                        )

                # Improvement suggestions
                st.markdown("---")
                st.header("💡 Resume Improvement Suggestions")

                if missing:
                    st.write(
                        "These job skills were not detected "
                        "in your uploaded resume:"
                    )

                    st.write(", ".join(missing))

                    st.info(
                        "If you have experience with these skills, "
                        "add truthful examples of how you used them. "
                        "Otherwise, consider learning the relevant skills."
                    )

                else:
                    st.success(
                        "All recognized job skills were found "
                        "in your resume!"
                    )

                if score >= 80:
                    st.success(
                        "Strong keyword overlap with the "
                        "recognized job skills."
                    )

                elif score >= 50:
                    st.info(
                        "Moderate keyword overlap. Review "
                        "the missing skills above."
                    )

                else:
                    st.warning(
                        "Low keyword overlap. Check whether "
                        "your relevant experience is clearly described."
                    )

                # Download report
                report = (
                    "AI RESUME ANALYZER REPORT\n\n"
                    f"Skill Match: {score:.1f}%\n\n"
                    "Matching Skills:\n"
                    + ", ".join(matching)
                    + "\n\nMissing Skills:\n"
                    + ", ".join(missing)
                    + "\n\nNote: Keyword-based analysis, "
                    "not an official ATS score."
                )

                st.download_button(
                    "📥 Download Analysis Report",
                    data=report,
                    file_name="resume_analysis_report.txt",
                    mime="text/plain"
                )

            else:
                st.info(
                    "No recognized skills found in "
                    "the job description."
                )

            # Extracted text
            with st.expander("📄 View Extracted Resume Text"):
                st.text_area(
                    "Extracted PDF Content",
                    text,
                    height=300
                )


# Footer
st.markdown("""
<div class="footer">
    AI Resume Analyzer | Built with Python, Streamlit and PyMuPDF
    <p>Keyword-Based Resume Analysis Project</p>
</div>
""", unsafe_allow_html=True)
