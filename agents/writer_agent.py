import os

from a2a.server.agent_execution import AgentExecutor
from a2a.server.events import EventQueue
from a2a.server.agent_execution import RequestContext
from a2a.helpers import new_text_message
from a2a.types import Role
from common.a2a_server import build_card, build_a2a_app

def write_article(prompt: str) -> str:
    return (
        "TECHNICAL ARTICLE\n\n"
        f"Topic: {prompt}\n\n"
        "Introduction\n"
        "Agent-to-Agent communication allows independently hosted agents to collaborate "
        "through a standardized protocol rather than sharing an internal workflow state.\n\n"
        "Architecture\n"
        "A supervisor can discover a specialist through its Agent Card, send a task over "
        "A2A, receive the result, and continue its own orchestration.\n\n"
        "Security\n"
        "Use TLS, strong workload authentication, authorization, Agent Card trust validation, "
        "timeouts, retries, rate limits, structured audit logs, and least-privilege identities.\n\n"
        "Conclusion\n"
        "LangGraph and A2A complement one another: LangGraph manages workflow and reasoning, "
        "while A2A provides interoperable communication between independently deployed agents."
    )

class WriterExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue):
        prompt = context.get_user_input()
        await event_queue.enqueue_event(
            new_text_message(write_article(prompt), role=Role.ROLE_AGENT)
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        return

card = build_card(
    "Writer Agent",
    "Independent technical writing specialist exposed over A2A.",
    os.getenv("WRITER_AGENT_CARD_URL", "http://127.0.0.1:8002"),
    "writer",
    "Technical Writing",
    ["Write a technical article about A2A.", "Turn research into documentation."]
)

app = build_a2a_app(card, WriterExecutor())

