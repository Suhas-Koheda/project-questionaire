from graph.state import ChatState
from langchain_google_genai import ChatGoogleGenerativeAI

def generate_behavioral(state: ChatState) -> dict:
    print("--- Generating Behavioral Questions ---")
    
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0.5)
    
    prompt = f"""
    You are an HR/Managerial interviewer. 
    Based on the candidate's Resume and the Job Description, generate n behavioral questions (situation/task based).
    
    Resume: {state["resume"]}
    Job Description: {state["jd"]}
    
    Return ONLY the questions, numbered 1 to n.
    """
    
    response = llm.invoke(prompt)
    
    return {"behavioral_questions": response.content}