from graph.state import ChatState
from langchain_google_genai import ChatGoogleGenerativeAI

def generate_hld(state: ChatState) -> dict:
   
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        temperature=0.5,
        google_api_key=state.get("gemini_api_key")
    )
    
   
    prompt = f"""
    You are a strict technical interviewer. 
    Based on the candidate's Resume, the Job Description, and the provided Project Code, generate beginner to advanced High-Level Design (HLD) interview questions.
    
    Resume: {state["resume"]}
    Job Description: {state["jd"]}
    Project Code: {state["project_code"]}
    
    Return ONLY the questions, numbered 1 to n.
    You need not complicate the things and also make sure that the questions are relevant to the candidate's resume and the job description.
    """
    
    
    response = llm.invoke(prompt)
    
    
    return {"hld_questions": response.content}