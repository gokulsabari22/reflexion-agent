from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field

class Reflection(BaseModel):
    missing: str = Field(description="Critique of what is missing.")
    superfluous: str = Field(description="Critique of what is superfluous")

class AnswerQuestion(BaseModel):
    """Answer the question."""
    answer: str = Field(description="250 words detailed answer to the question")
    reflection: Reflection = Field(description="Your reflecrtion on the initial answer")
    search_queries: List[str] = Field(description="You should definetly recommend atleast one or more search queries to research information and improve your answer.")

class ReviseAnswer(AnswerQuestion):
    references: List[str] = Field(description="Reference from where the answer is taken")