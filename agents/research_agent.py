from a2a.server.agent_execution import AgentExecutor
from a2a.server.events import EventQueue
from a2a.server.agent_execution import RequestContext
from a2a.helpers import new_text_message
from a2a.types import Role
from common.a2a_server import build_card, build_a2a_app

def research(topic: str) -> str:
    # Replace this deterministic demo with a real search/RAG/LLM pipeline.
    return (
        f"Research findings for: {topic}\n\n"
        "1. A2A separates network communication from agent reasoning.\n"
        "2. Each agent can expose an Agent Card describing identity, skills and transports.\n"
        "3. JSON-RPC over HTTP is suitable for interoperable request/response communication.\n"
        "4. Production systems should authenticate every hop and validate discovered Agent Cards.\n"
        "5. LangGraph can orchestrate delegation while the specialist remains an independent service."
    )

class ResearchExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue):
        text = context.get_user_input()
        result = research(text)
        await event_queue.enqueue_event(
            new_text_message(result, role=Role.ROLE_AGENT)
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        return

card = build_card(
    "Research Agent",
    "Independent research specialist exposed over A2A.",
    "http://127.0.0.1:8001",
    "research",
    "Technical Research",
    ["Research LangGraph A2A security.", "Find architecture considerations."]
)

app = build_a2a_app(card, ResearchExecutor())
