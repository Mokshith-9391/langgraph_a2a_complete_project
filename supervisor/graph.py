from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from .a2a_client import call_agent
from common.config import A2A_API_KEY, RESEARCH_URL, WRITER_URL

class State(TypedDict, total=False):
    user_request: str
    research: str
    article: str

async def research_node(state: State):
    result = await call_agent(
        RESEARCH_URL,
        state["user_request"],
        A2A_API_KEY,
    )
    return {"research": result}

async def writer_node(state: State):
    prompt = (
        f"Original request: {state['user_request']}\n\n"
        f"Research supplied by the remote Research Agent:\n{state['research']}"
    )
    result = await call_agent(WRITER_URL, prompt, A2A_API_KEY)
    return {"article": result}

builder = StateGraph(State)
builder.add_node("research", research_node)
builder.add_node("writer", writer_node)
builder.add_edge(START, "research")
builder.add_edge("research", "writer")
builder.add_edge("writer", END)
graph = builder.compile()
