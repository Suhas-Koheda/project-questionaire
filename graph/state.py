from typing import TypedDict, List, Annotated
from langchain_core.messages import BaseMessage
import operator
class ChatState(TypedDict):
    proj: str
    summary: str
    project_code: str  
    resume: str
    jd: str
    messages: Annotated[List[BaseMessage], operator.add]
    hld_questions: str
    lld_questions: str
    behavioral_questions: str
    project_specific_questions: str  
    repo_source:str
    gemini_cache_id: str
    gemini_api_key: str