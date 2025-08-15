"""Tests for agent graph."""

from agent_core.graph import AgentGraph


def test_agent_graph_exists() -> None:
    """Graph can be instantiated."""
    assert AgentGraph() is not None
