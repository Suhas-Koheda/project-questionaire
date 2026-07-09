from graph.state import ChatState
from langchain_google_genai import ChatGoogleGenerativeAI

def generate_project_specific(state: ChatState) -> dict:
    print("--- Generating Project-Specific Questions ---")
    
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0.3)
    
    prompt = f"""
    You are a strict Senior Engineer reviewing a candidate's code. 
    You must deeply analyze the provided Project Code and Summary.
    
    Resume: {state["resume"]}
    Job Description: {state["jd"]}
    Project Code: {state["project_code"]}
    
    Do NOT ask generic questions. Ask specific questions like:
    - "Why did you choose this specific design pattern here?"
    - "What happens in this code block if there is a sudden spike in traffic?"
    - "Why is this specific library used instead of X?"
    - "Explain the data flow between these two specific functions."
    
    
    
    Return ONLY n highly specific project-related questions, numbered 1 to n.
    never hallucinate things
    """
    
    response = llm.invoke(prompt)
    
    return {"project_specific_questions": response.content}