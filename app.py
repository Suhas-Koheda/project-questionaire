import argparse
import google.generativeai as genai
from langgraph.graph import StateGraph, END

from graph.state import ChatState
from nodes.input_node import ingest_data_node
from nodes.cache_node import cache_project_data
from nodes.hld_node import generate_hld
from nodes.lld_node import generate_lld
from nodes.behavioural_node import generate_behavioral
from nodes.project_node import generate_project_specific
from utils.readpdf import read_pdf

import os
from dotenv import load_dotenv
load_dotenv()

def build_graph():
    workflow = StateGraph(ChatState)

    workflow.add_node("ingest_node", ingest_data_node)
    workflow.add_node("hld_node", generate_hld)
    workflow.add_node("lld_node", generate_lld)
    workflow.add_node("behavioral_node", generate_behavioral)
    workflow.add_node("project_node", generate_project_specific)

    workflow.set_entry_point("ingest_node")

    workflow.add_edge("ingest_node", "hld_node")
    workflow.add_edge("ingest_node", "lld_node")
    workflow.add_edge("ingest_node", "behavioral_node")
    workflow.add_edge("ingest_node", "project_node")

    workflow.add_edge("hld_node", END)
    workflow.add_edge("lld_node", END)
    workflow.add_edge("behavioral_node", END)
    workflow.add_edge("project_node", END)

    return workflow.compile()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Interview Questions")
    parser.add_argument("--repo", required=True, help="Project URL or local path")
    parser.add_argument("--resume", required=True, help="Path to resume file")
    parser.add_argument("--jd", required=True, help="Path to Job Description file")
    parser.add_argument("--name", required=True, help="Project name")
    parser.add_argument("--api-key", required=False, default="", help="Gemini API Key")
    
    args = parser.parse_args()

    cli_key = args.api_key or os.environ.get("GEMINI_API_KEY", "")

    initial_state = {
        "proj": args.name,
        "summary": "",
        "project_code": "",
        "resume": args.resume,
        "jd": args.jd,
        "messages": [],
        "hld_questions": "",
        "lld_questions": "",
        "behavioral_questions": "",
        "project_specific_questions": "",
        "repo_source": args.repo,
        "gemini_cache_id": "",
        "gemini_api_key": cli_key
    }

    print(f"\n🚀 Starting Agent for Project: {args.name}\n")

    app = build_graph()
    final_state = app.invoke(initial_state)

    print("\n" + "="*50)
    print("✅ GENERATION COMPLETE")
    print("="*50)
    
    print("\n🎯 HIGH LEVEL DESIGN QUESTIONS:\n")
    print(final_state["hld_questions"][0]["text"])

    print("\n🔧 LOW LEVEL DESIGN QUESTIONS:\n")
    print(final_state["lld_questions"][0]["text"])

    print("\n🧠 PROJECT SPECIFIC QUESTIONS:\n")
    print(final_state["project_specific_questions"][0]["text"])

    print("\n🤝 BEHAVIORAL QUESTIONS:\n")
    print(final_state["behavioral_questions"][0]["text"])