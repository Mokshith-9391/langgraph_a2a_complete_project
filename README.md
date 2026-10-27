# LangGraph + A2A Complete Python Demo

A production-oriented learning project demonstrating:

- LangGraph supervisor orchestration
- Independent Research and Writer A2A agents
- A2A Agent Cards
- A2A JSON-RPC transport
- A2A v1.x Python SDK
- Async HTTP client discovery
- Multi-agent delegation over HTTP
- Basic API-key authentication middleware
- Health endpoints
- Docker Compose
- Local LLM integration point (optional)
- Tests

## Architecture

Client -> LangGraph Supervisor -> A2A Research Agent
                         |
                         +-------> A2A Writer Agent

Ports:
- Supervisor: 8000
- Research A2A: 8001
- Writer A2A: 8002

The specialist agents are independently hosted processes. They do NOT share LangGraph state.

## Important SDK note

This project targets the current A2A Python SDK 1.x API. The v1.0 server API uses route factories such as
`create_agent_card_routes()` and `create_jsonrpc_routes()`, and `create_client()` is used for clients.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Terminal 1
uvicorn agents.research_agent:app --host 0.0.0.0 --port 8001

# Terminal 2
uvicorn agents.writer_agent:app --host 0.0.0.0 --port 8002

# Terminal 3
uvicorn supervisor.app:app --host 0.0.0.0 --port 8000

# Terminal 4
python client.py
```

Then enter a request such as:

`Research LangGraph A2A security best practices and write a short technical article.`

## Docker

```bash
docker compose up --build
```

Then:

```bash
python client.py --supervisor http://localhost:8000
```

## Agent Cards

Open:

- http://localhost:8001/.well-known/agent-card.json
- http://localhost:8002/.well-known/agent-card.json

## Security

Set:

```bash
export A2A_API_KEY="change-me"
```

The supervisor sends `Authorization: Bearer <key>` to specialist agents.

For real production deployments also use TLS, an API gateway/service mesh, short-lived credentials, workload identity, rate limiting, audit logs, and signed/pinned Agent Cards.

## Optional real LLM

The demo intentionally works without an external LLM so it can run immediately. The specialist agents contain a clean `generate_*` function where you can integrate an OpenAI-compatible local endpoint, Ollama, vLLM, Bedrock, or another provider.

