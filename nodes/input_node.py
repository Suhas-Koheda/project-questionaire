import os
from gitingest import ingest
from graph.state import ChatState
from utils.readpdf import read_pdf

def _read_input_data(raw_input: str) -> str:
    """Helper to read a file if a path is given, otherwise return the raw text."""
    if raw_input.lower().endswith((".pdf", ".txt")) or raw_input.startswith(("/", "./", "../")):
        if not os.path.exists(raw_input):
            return raw_input
            
        if raw_input.lower().endswith(".pdf"):
            return read_pdf(raw_input)
        else:
            with open(raw_input, "r", encoding="utf-8") as f:
                return f.read()
    
    return raw_input

def ingest_data_node(state: ChatState) -> dict:
    print(f"Ingesting project from: {state['repo_source']}")
    
    resume_text = _read_input_data(state["resume"])
    jd_text = _read_input_data(state["jd"])
            
    summary, tree, code_content = ingest(state["repo_source"])
    
    full_project_code = f"Directory Structure:\n{tree}\n\nFiles Content:\n{code_content}"
    
    return {
        "resume": resume_text,
        "jd": jd_text,
        "summary": summary,
        "project_code": full_project_code
    }