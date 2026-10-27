from fastapi import FastAPI
from starlette.routing import Mount
from a2a.server.apps.jsonrpc.fastapi_app import A2AFastAPIApplication
from a2a.server.agent_execution import AgentExecutor
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.types import AgentCard, AgentCapabilities, AgentInterface, AgentSkill

def build_card(name: str, description: str, url: str, skill_id: str, skill_name: str, examples: list[str]):
    skill = AgentSkill(
        id=skill_id,
        name=skill_name,
        description=description,
        tags=[skill_id, "a2a", "agent"],
        examples=examples,
        input_modes=["text/plain"],
        output_modes=["text/plain"],
    )
    return AgentCard(
        name=name,
        description=description,
        supported_interfaces=[
            AgentInterface(
                protocol_binding="JSONRPC",
                protocol_version="1.0",
                url=f"{url}/a2a/jsonrpc",
            )
        ],
        version="1.0.0",
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain"],
        capabilities=AgentCapabilities(streaming=False, push_notifications=False),
        skills=[skill],
    )

def build_a2a_app(agent_card: AgentCard, executor: AgentExecutor):
    task_store = InMemoryTaskStore()
    handler = DefaultRequestHandler(
        agent_executor=executor,
        task_store=task_store,
        agent_card=agent_card,
    )

    # The SDK's FastAPI application wrapper is intentionally avoided for the
    # protocol routes; route factories are used as in the v1.x API.
    app = FastAPI(title=agent_card.name, version=agent_card.version)

    app.add_api_route("/health", lambda: {"status": "ok", "agent": agent_card.name}, methods=["GET"])
    for route in create_agent_card_routes(agent_card):
        app.router.routes.append(route)

    for route in create_jsonrpc_routes(
        request_handler=handler,
        rpc_url="/a2a/jsonrpc",
        enable_v0_3_compat=False,
    ):
        app.router.routes.append(route)

    return app
