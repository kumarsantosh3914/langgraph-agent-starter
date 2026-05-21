from typing import Annotated, List, Any, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

class EvaluatorOutput(BaseModel):
    feedback: str = Field(description="Feedback on the user's interview answer")
    score: int = Field(description="Score from 1-10 on answer quality")
    needs_improvement: bool = Field(description="Whether the answer needs significant improvement")
    user_input_needed: bool = Field(description="True if the coach needs more input or clarification from the user")

class State(TypedDict):
    messages: Annotated[List[Any], add_messages]
    success_criteria: str
    feedback_on_work: Optional[str]
    success_criteria_met: bool
    user_input_needed: bool