import streamlit as st
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
ENV_GROQ_KEY = os.getenv("GROQ_API_KEY", "")
ENV_GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

# Internal Modules
from modules.parser import parse_resume, parse_jd
from modules.analyzer import analyze_resume_vs_jd
from modules.rewriter import rewrite_full_resume_html
# from modules.exporter import export_html_to_pdf
from modules.exporter import export_html_to_pdf

# External Clients
import ollama
import streamlit.components.v1 as components


# ======================================================
# Streamlit UI Setup
# ======================================================
st.set_page_config(page_title="AI Resume Analyzer + Rewriter", layout="wide")
st.title("🔥 AI Resume Analyzer + HTML Resume Generator")

tabs = st.tabs(["📄 Resume ↔ JD Analyzer", "✍️ HTML Resume Rewriter"])



# ======================================================
# Sidebar — Provider + Keys
# ======================================================
st.sidebar.header("⚙️ LLM Provider & API Keys")

provider = st.sidebar.radio(
    "Choose Provider",
    ["ollama", "groq", "gemini"],
)

if provider == "groq":
    groq_key = st.sidebar.text_input("Groq API Key", value=ENV_GROQ_KEY, type="password")
    gemini_key = ""

elif provider == "gemini":
    gemini_key = st.sidebar.text_input("Gemini API Key", value=ENV_GEMINI_KEY, type="password")
    groq_key = ""

else:
    groq_key = ""
    gemini_key = ""



# Fetch Ollama model list
def fetch_ollama_models():
    try:
        return sorted([m["name"] for m in ollama.list()["models"]])
    except:
        return ["mistral", "llama3", "mixtral"]




# ======================================================
# TAB 1 — ANALYZER
# ======================================================
with tabs[0]:

    st.header("1️⃣ Upload Resume & Job Description")

    col1, col2 = st.columns(2)

    with col1:
        resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])

    with col2:
        jd_file = st.file_uploader("Upload Job Description", type=["pdf", "docx", "txt"])


    # MODEL SELECTION
    st.header("2️⃣ Select Model")

    if provider == "gemini":
        model_list = ["gemini-2.0-flash"]

    elif provider == "groq":
        model_list = ["llama-3.3-70b-versatile"]

    else:
        model_list = fetch_ollama_models()

    model = st.selectbox("Available Model", model_list)


    # RUN ANALYSIS
    if st.button("Analyze Resume vs JD", type="primary", use_container_width=True):

        if not resume_file or not jd_file:
            st.error("Please upload both Resume and JD.")
            st.stop()

        resume_text = parse_resume(resume_file)
        jd_text = parse_jd(jd_file)

        if not resume_text.strip() or not jd_text.strip():
            st.error("Parsing failed. Try TXT for debugging.")
            st.stop()

        # Persist for rewriter
        st.session_state.resume_text = resume_text
        st.session_state.jd_text = jd_text
        st.session_state.provider = provider
        st.session_state.model = model
        st.session_state.groq_key = groq_key
        st.session_state.gemini_key = gemini_key

        st.success("✓ Files parsed successfully!")

        st.header("3️⃣ LLM ATS Analysis")

        with st.spinner("Analyzing resume vs JD using LLM…"):
            result = analyze_resume_vs_jd(
                resume_text=resume_text,
                jd_text=jd_text,
                provider=provider,
                model=model,
                groq_api_key=groq_key,
                gemini_api_key=gemini_key
            )

        if "error" in result:
            st.error(result["error"])
            st.stop()

        # Save analysis
        st.session_state.analysis_done = True
        st.session_state.analysis_result = result
        st.session_state.matched_skills = result["matched_skills"]
        st.session_state.missing_skills = result["missing_skills"]
        st.session_state.fit_score = result["fit_score"]

        # Display Results
        col1, col2, col3 = st.columns(3)
        col1.metric("ATS Score", result["ats_score"])
        col2.metric("Fit Score", result["fit_score"])
        col3.metric("Keyword Coverage", result["keyword_coverage"])

        st.subheader("Matched Skills")
        st.write(", ".join(result["matched_skills"]))

        st.subheader("Missing Skills")
        st.write(", ".join(result["missing_skills"]))

        st.subheader("Summary Alignment")
        st.write(result["summary_alignment"])

        st.subheader("Experience Alignment")
        st.write(result["experience_alignment"])

        st.subheader("Red Flags")
        st.write(result["red_flags"])

        st.subheader("Recommendations to Improve Resume")
        st.write(result["recommendations"])

        # Debug
        st.markdown("---")
        with st.expander("📄 Parsed Resume"):
            st.text(resume_text)
        with st.expander("📄 Parsed JD"):
            st.text(jd_text)



# ======================================================
# TAB 2 — HTML RESUME REWRITER
# ======================================================
with tabs[1]:

    st.header("✍️ Generate Fully Rewritten HTML Resume")

    if "analysis_done" not in st.session_state:
        st.info("Run the Analyzer first in Tab 1.")
        st.stop()

    # Template selection
    template = st.selectbox(
        "Select Resume Template",
        ["minimal", "professional", "modern"],
        index=1
    )

    if st.button("Generate HTML Resume", type="primary"):

        with st.spinner("Rewriting resume using selected LLM…"):
            html_resume = rewrite_full_resume_html(
                resume_text=st.session_state.resume_text,
                jd_text=st.session_state.jd_text,
                matched_skills=st.session_state.matched_skills,
                missing_skills=st.session_state.missing_skills,
                similarity_score=st.session_state.fit_score,
                provider=st.session_state.provider,
                model=st.session_state.model,
                template=template,
                groq_api_key=st.session_state.groq_key,
                gemini_api_key=st.session_state.gemini_key,
            )
            st.session_state.rewritten_resume_html = html_resume

    html_code = st.session_state.get("rewritten_resume_html", "")

    # Preview + Editor
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Live HTML Resume Preview")
        components.html(html_code, height=650, scrolling=True)

    with col2:
        st.subheader("HTML Code (Editable)")
        edited = st.text_area("Edit HTML", value=html_code, height=650)
        st.session_state.rewritten_resume_html = edited

    st.markdown("---")

    # === Export ===
    if html_code.strip():
        os.makedirs("outputs", exist_ok=True)

        # Save HTML
        html_path = "outputs/final_resume.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_code)

        with open(html_path, "rb") as f:
            st.download_button(
                "⬇ Download HTML Resume",
                f.read(),
                file_name="resume.html",
                mime="text/html"
            )

        # Save PDF using pure-Python ReportLab exporter
        pdf_path = "outputs/final_resume.pdf"
        export_html_to_pdf(html_code, pdf_path)

        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "⬇ Download PDF Resume",
                    f.read(),
                    file_name="resume.pdf",
                    mime="application/pdf"
                )
