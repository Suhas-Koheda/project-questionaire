import streamlit as st
import os
import shutil
from app import build_graph

st.set_page_config(
    page_title="AI Technical Interview Prep Kit Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #1e1b4b 0%, #0f172a 50%, #020617 100%);
}
div.stButton > button:first-child {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    color: white;
    font-weight: 600;
    border-radius: 8px;
    border: none;
    padding: 12px 28px;
    box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.4);
    transition: all 0.3s ease;
    width: 100%;
}
div.stButton > button:first-child:hover {
    background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
    box-shadow: 0 6px 20px 0 rgba(99, 102, 241, 0.6);
    transform: translateY(-2px);
}
.header-title {
    font-family: 'Outfit', 'Inter', sans-serif;
    font-weight: 800;
    font-size: 3rem;
    background: linear-gradient(to right, #818cf8, #c084fc, #e879f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.5rem;
}
.header-subtitle {
    text-align: center;
    font-size: 1.2rem;
    color: #94a3b8;
    margin-bottom: 2rem;
}
.result-card {
    background: rgba(30, 41, 59, 0.45);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
}
.tab-header {
    font-size: 1.5rem;
    font-weight: 700;
    color: #f1f5f9;
    border-bottom: 2px solid #6366f1;
    padding-bottom: 8px;
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-title">Interview Prep Kit Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">Analyze repositories, resumes, and job descriptions to generate tailored technical questions</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Configuration")
    project_name = st.text_input("Project Name", value="Deepseek Project")
    repo_source = st.text_input("Repository Source (GitHub URL or Local Path)", value="https://github.com/Suhas-Koheda/Deepseek")
    gemini_key = st.text_input("Gemini API Key", type="password", value=st.session_state.get("gemini_api_key", ""))
    if gemini_key:
        st.session_state["gemini_api_key"] = gemini_key
    
    st.markdown("---")
    st.markdown("### Inputs")
    
    resume_type = st.radio("Resume Input Method", ["Upload File", "Paste Text"])
    resume_data = ""
    if resume_type == "Upload File":
        resume_file = st.file_uploader("Upload Resume (PDF or TXT)", type=["pdf", "txt"])
        if resume_file:
            resume_data = resume_file
    else:
        resume_data = st.text_area("Paste Resume Text", height=200)

    st.markdown("---")
    jd_type = st.radio("Job Description Input Method", ["Upload File", "Paste Text"])
    jd_data = ""
    if jd_type == "Upload File":
        jd_file = st.file_uploader("Upload Job Description (PDF or TXT)", type=["pdf", "txt"])
        if jd_file:
            jd_data = jd_file
    else:
        jd_data = st.text_area("Paste Job Description Text", height=200)

    st.markdown("---")
    generate_btn = st.button("Generate Interview Prep Kit 🚀")

if generate_btn:
    if not gemini_key:
        st.error("Please provide a Gemini API Key.")
    elif not repo_source:
        st.error("Please provide a repository source.")
    elif not resume_data:
        st.error("Please provide a resume.")
    elif not jd_data:
        st.error("Please provide a job description.")
    else:
        temp_resume_path = ""
        temp_jd_path = ""
        
        try:
            if isinstance(resume_data, str):
                resume_input = resume_data
            else:
                temp_resume_path = f"temp_resume_{resume_data.name}"
                with open(temp_resume_path, "wb") as f:
                    f.write(resume_data.getbuffer())
                resume_input = temp_resume_path

            if isinstance(jd_data, str):
                jd_input = jd_data
            else:
                temp_jd_path = f"temp_jd_{jd_data.name}"
                with open(temp_jd_path, "wb") as f:
                    f.write(jd_data.getbuffer())
                jd_input = temp_jd_path

            initial_state = {
                "proj": project_name,
                "summary": "",
                "project_code": "",
                "resume": resume_input,
                "jd": jd_input,
                "messages": [],
                "hld_questions": "",
                "lld_questions": "",
                "behavioral_questions": "",
                "project_specific_questions": "",
                "repo_source": repo_source,
                "gemini_cache_id": "",
                "gemini_api_key": gemini_key
            }

            with st.spinner("Analyzing project repository, parsing files, and generating comprehensive interview prep questions..."):
                app_graph = build_graph()
                final_state = app_graph.invoke(initial_state)

            st.success("🎉 Successfully Generated Prep Kit!")

            hld_text = ""
            if isinstance(final_state["hld_questions"], list) and len(final_state["hld_questions"]) > 0:
                hld_text = final_state["hld_questions"][0]["text"]
            else:
                hld_text = str(final_state["hld_questions"])

            lld_text = ""
            if isinstance(final_state["lld_questions"], list) and len(final_state["lld_questions"]) > 0:
                lld_text = final_state["lld_questions"][0]["text"]
            else:
                lld_text = str(final_state["lld_questions"])

            proj_text = ""
            if isinstance(final_state["project_specific_questions"], list) and len(final_state["project_specific_questions"]) > 0:
                proj_text = final_state["project_specific_questions"][0]["text"]
            else:
                proj_text = str(final_state["project_specific_questions"])

            behave_text = ""
            if isinstance(final_state["behavioral_questions"], list) and len(final_state["behavioral_questions"]) > 0:
                behave_text = final_state["behavioral_questions"][0]["text"]
            else:
                behave_text = str(final_state["behavioral_questions"])

            tab1, tab2, tab3, tab4 = st.tabs([
                "🎯 High-Level Design",
                "🔧 Low-Level Design",
                "🧠 Project-Specific",
                "🤝 Behavioral"
            ])

            with tab1:
                st.markdown('<div class="tab-header">High-Level Design (HLD) Questions</div>', unsafe_allow_html=True)
                st.markdown(hld_text)
                st.download_button("Download HLD Questions", hld_text, file_name="hld_questions.md")

            with tab2:
                st.markdown('<div class="tab-header">Low-Level Design (LLD) Questions</div>', unsafe_allow_html=True)
                st.markdown(lld_text)
                st.download_button("Download LLD Questions", lld_text, file_name="lld_questions.md")

            with tab3:
                st.markdown('<div class="tab-header">Project-Specific Questions</div>', unsafe_allow_html=True)
                st.markdown(proj_text)
                st.download_button("Download Project Questions", proj_text, file_name="project_questions.md")

            with tab4:
                st.markdown('<div class="tab-header">Behavioral Questions</div>', unsafe_allow_html=True)
                st.markdown(behave_text)
                st.download_button("Download Behavioral Questions", behave_text, file_name="behavioral_questions.md")

        except Exception as e:
            st.error(f"An error occurred during generation: {e}")
        finally:
            if temp_resume_path and os.path.exists(temp_resume_path):
                os.remove(temp_resume_path)
            if temp_jd_path and os.path.exists(temp_jd_path):
                os.remove(temp_jd_path)
else:
    st.info("👈 Use the sidebar to fill in repository and document inputs, then click Generate.")
