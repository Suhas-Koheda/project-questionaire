import google.generativeai as genai
from graph.state import ChatState


def cache_project_data(state: ChatState) -> dict:

    
   
    text_to_cache = f"""
    Resume: {state["resume"]}
    JD: {state["jd"]}
    Project Code: {state["project_code"]}
    """
    
   
    cache = genai.caching.CachedContent.create(
        model="gemini-3.1-pro-preview",
        display_name="project_context",
        system_instruction="You are an expert technical interviewer.",
        contents=[text_to_cache]
    )
    return {"gemini_cache_id": cache.name}