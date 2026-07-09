from graph.state import ChatState
from langchain_google_genai import ChatGoogleGenerativeAI

def generate_lld(state: ChatState) -> dict:
    print("--- Generating LLD Questions ---")
    
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0.5, google_api_key=state.get("gemini_api_key"))
    
    prompt = f"""
    You are a strict technical interviewer. 
    Based on the candidate's Resume, the Job Description, and the provided Project Code, generate n number of Low-Level Design (LLD) / Class Diagram / API Design questions.
    
    Resume: {state["resume"]}
    Job Description: {state["jd"]}
    Project Code: {state["project_code"]}
    
    Return ONLY the questions, numbered 1 to n.
    """
    
    response = llm.invoke(prompt)
    
    return {"lld_questions": response.content}