"""Tests for agent graph."""

import pytest

from agent_core.graph import AgentGraph


def test_agent_handles_shell_instruction() -> None:
    """AgentGraph delegates shell commands to the shell runner."""

    captured: list[list[str]] = []

    def fake_shell_runner(command: list[str]) -> str:
        captured.append(list(command))
        return "done"

    agent = AgentGraph(shell_runner=fake_shell_runner)
    result = agent.handle_instruction("Run shell command: echo 'hi'")

    assert result == "done"
    assert captured == [["echo", "hi"]]


def test_agent_parses_backtick_command() -> None:
    """Backtick-wrapped commands are supported."""

    agent = AgentGraph(shell_runner=lambda cmd: "".join(cmd))
    result = agent.handle_instruction("Please execute shell command `printf foo`")

    assert result == "printffoo"


def test_agent_rejects_unrelated_instruction() -> None:
    """Non-shell instructions raise an error for now."""

    agent = AgentGraph()

    with pytest.raises(ValueError):
        agent.handle_instruction("Summarize the latest logs")
