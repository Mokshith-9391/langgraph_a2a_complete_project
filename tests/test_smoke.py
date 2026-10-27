from agents.research_agent import research
from agents.writer_agent import write_article

def test_research():
    assert "A2A" in research("LangGraph A2A")

def test_writer():
    assert "TECHNICAL ARTICLE" in write_article("A2A")
