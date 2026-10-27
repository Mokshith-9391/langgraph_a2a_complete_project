import uuid
import httpx
from a2a.client import A2ACardResolver, create_client
from a2a.types import Message, Part, Role, SendMessageRequest

async def call_agent(agent_url: str, text: str, api_key: str | None = None) -> str:
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    async with httpx.AsyncClient(timeout=120, headers=headers) as http:
        resolver = A2ACardResolver(http, agent_url)
        card = await resolver.get_agent_card()
        client = await create_client(card)

        message = Message(
            role=Role.ROLE_USER,
            message_id=str(uuid.uuid4()),
            context_id=str(uuid.uuid4()),
            parts=[Part(text=text)],
        )

        request = SendMessageRequest(message=message)
        outputs = []

        async for event in client.send_message(request):
            if event.HasField("message"):
                for part in event.message.parts:
                    if part.HasField("text"):
                        outputs.append(part.text)
            elif event.HasField("artifact_update"):
                artifact = event.artifact_update.artifact
                for part in artifact.parts:
                    if part.HasField("text"):
                        outputs.append(part.text)

        return "\n".join(outputs).strip()
