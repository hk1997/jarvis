import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ai_engine.agents.news_aggregator_agent import NewsAggregatorAgent
from ai_engine.common import LLMInterface


class DummyLLM(LLMInterface):
    def __init__(self, response: str) -> None:
        self.response = response
        self.last_messages = None

    def send_prompt(self, messages, **kwargs):
        self.last_messages = messages
        return self.response


def test_generate_daily_digest():
    expected = {
        "Global Headlines": ["gh"],
        "Finance & Economy": ["fe"],
        "Politics": {"US": ["us"], "UK": ["uk"], "India": ["in"]},
        "Sports": ["sp"],
        "Science & Tech": ["st"],
    }

    llm = DummyLLM(json.dumps(expected))
    agent = NewsAggregatorAgent(llm=llm)
    result = agent.generate_daily_digest()

    assert result == expected
    assert llm.last_messages[0]["role"] == "system"
    assert "Politics" in expected

