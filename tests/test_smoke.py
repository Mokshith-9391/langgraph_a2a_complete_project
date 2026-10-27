import importlib

from agents.research_agent import research
from agents.writer_agent import write_article

def test_research():
    assert "A2A" in research("LangGraph A2A")

def test_writer():
    assert "TECHNICAL ARTICLE" in write_article("A2A")


def test_research_agent_card_uses_local_default(monkeypatch):
    monkeypatch.delenv("RESEARCH_AGENT_CARD_URL", raising=False)
    import agents.research_agent as research_agent

    reloaded = importlib.reload(research_agent)
    assert reloaded.card.supported_interfaces[0].url == "http://127.0.0.1:8001/a2a/jsonrpc"


def test_research_agent_card_uses_environment_url(monkeypatch):
    monkeypatch.setenv("RESEARCH_AGENT_CARD_URL", "http://research-agent:8001")
    import agents.research_agent as research_agent

    reloaded = importlib.reload(research_agent)
    assert reloaded.card.supported_interfaces[0].url == "http://research-agent:8001/a2a/jsonrpc"


def test_writer_agent_card_uses_local_default(monkeypatch):
    monkeypatch.delenv("WRITER_AGENT_CARD_URL", raising=False)
    import agents.writer_agent as writer_agent

    reloaded = importlib.reload(writer_agent)
    assert reloaded.card.supported_interfaces[0].url == "http://127.0.0.1:8002/a2a/jsonrpc"


def test_writer_agent_card_uses_environment_url(monkeypatch):
    monkeypatch.setenv("WRITER_AGENT_CARD_URL", "http://writer-agent:8002")
    import agents.writer_agent as writer_agent

    reloaded = importlib.reload(writer_agent)
    assert reloaded.card.supported_interfaces[0].url == "http://writer-agent:8002/a2a/jsonrpc"
