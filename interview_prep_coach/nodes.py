from typing import Any, Dict, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# pyrefly: ignore [missing-import]
from models import EvaluatorOutput, State
# pyrefly: ignore [missing-import]
from tools import tools

# LLMs
worker_llm = ChatOpenAI(model="gpt-4o-mini")
worker_llm_with_tools = worker_llm.bind_tools(tools)

evaluator_llm = ChatOpenAI(model="gpt-4o-mini")
evaluator_llm_with_output = evaluator_llm.with_structured_output(EvaluatorOutput)

# Helper
def format_conversation(messages: List[Any]) -> str:
    conversation = ""
    for msg in messages:
        if isinstance(msg, HumanMessage):
            conversation += f"User: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            text = msg.content or "[tool use]"
            conversation += f"Coach: {text}\n"
    return conversation

# Nodes
def worker(state: State) -> Dict[str, Any]:
    system_message = f"""You are an expert technical interview prep coach. You have access to web search and Wikipedia tools.
 
When a user tells you a company and role:
1. Research the company using your tools to understand their tech stack, engineering culture, and common interview patterns.
2. Generate exactly 5 tailored interview questions based on your research.
3. For each question, include a brief explanation of *why* this question is relevant for this company/role and a quick tip on how to structure a good answer.
4. Do NOT dump raw Wikipedia summaries about the company. Just dive straight into the coaching and the tailored questions.
 
When the user answers a question, provide detailed, constructive feedback, score their answer, and suggest specific improvements.
 
Success criteria: {state['success_criteria']}
 
If you have a clarifying question for the user, clearly state it.
Otherwise reply with your final answer."""

    if state.get("feedback_on_work"):
        system_message += f"""
An internal evaluator reviewed your previous draft and rejected it with the following feedback: 
{state['feedback_on_work']}

Please improve your response based on this feedback. 
CRITICAL: Do NOT mention this internal feedback, do NOT apologize, and do NOT thank anyone for the feedback in your new response. Just output the improved response directly to the user."""

    messages = state["messages"]
    found_system = False
    for msg in messages:
        if isinstance(msg, SystemMessage):
            msg.content = system_message
            found_system = True
    if not found_system:
        messages = [SystemMessage(content=system_message)] + messages

    response = worker_llm_with_tools.invoke(messages)
    return {"messages": [response]}

def evaluator(state: State) -> State:
    last_response = state["messages"][-1].content

    system_message = """You are an evaluator for an interview prep coach.
Assess whether the coach's response is helpful, accurate, and meets the success criteria.
Score the response and decide if it needs improvement."""

    user_message = f"""Conversation so far:
{format_conversation(state['messages'])}
 
Success criteria: {state['success_criteria']}
 
Coach's latest response: {last_response}
 
Evaluate this response. Decide if success criteria are met or if more user input is needed."""
    
    if state.get("feedback_on_work"):
        user_message += f"\nPrior feedback: {state['feedback_on_work']}"
        user_message += "\nIf the coach keeps repeating mistakes, set user_input_needed to true."
    
    eval_result = evaluator_llm_with_output.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content=user_message)
    ])

    return {
        "messages": [{"role": "assistant", "content": f"Evaluator (Score: {eval_result.score}/10): {eval_result.feedback}"}],
        "feedback_on_work": eval_result.feedback,
        "success_criteria_met": not eval_result.needs_improvement,
        "user_input_needed": eval_result.user_input_needed,
    }

# Routers
def worker_router(state: State) -> str:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "evaluator"

def route_after_eval(state: State) -> str:
    if state["success_criteria_met"] or state["user_input_needed"]:
        return "END"
    return "worker"