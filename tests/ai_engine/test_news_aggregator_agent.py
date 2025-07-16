import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ai_engine.agents.news_aggregator_agent import NewsAggregatorAgent


def test_generate_daily_digest(monkeypatch):
    expected = {
        "Global Headlines": ["gh"],
        "Finance & Economy": ["fe"],
        "Politics": {"US": ["us"], "UK": ["uk"], "India": ["in"]},
        "Sports": ["sp"],
        "Science & Tech": ["st"],
    }

    def mock_send_prompt(messages, **kwargs):
        mock_send_prompt.last_messages = messages
        return json.dumps(expected)

    monkeypatch.setattr("ai_engine.agents.news_aggregator_agent.send_prompt", mock_send_prompt)

    agent = NewsAggregatorAgent()
    result = agent.generate_daily_digest()

    assert result == expected
    assert mock_send_prompt.last_messages[0]["role"] == "system"
    assert "Politics" in expected

