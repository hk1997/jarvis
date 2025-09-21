"""Integration tests for FastAPI app."""

from fastapi.testclient import TestClient

from agent_core.graph import AgentGraph
from agent_core.tools.shell import ShellCommandError
from server.app import InstructionRequest, app


def test_run_instruction_success() -> None:
    """Agent executes shell-related instruction through the API."""

    def fake_runner(command: list[str]) -> str:
        assert command == ["echo", "hello"]
        return "hello\n"

    app.state.agent = AgentGraph(shell_runner=fake_runner)

    client = TestClient(app)
    response = client.post(
        "/agent/run",
        json=InstructionRequest(instruction="Run shell command: echo hello").model_dump(),
    )

    assert response.status_code == 200
    assert response.json() == {"output": "hello\n"}


def test_run_instruction_invalid_request() -> None:
    """Non-shell instructions get rejected."""

    client = TestClient(app)
    response = client.post(
        "/agent/run",
        json={"instruction": "Summarize the logs"},
    )

    assert response.status_code == 400


def test_run_instruction_shell_error() -> None:
    """Shell errors surface as HTTP 500 with details."""

    def failing_runner(command: list[str]) -> str:
        raise ShellCommandError(command, 2, "permission denied")

    app.state.agent = AgentGraph(shell_runner=failing_runner)

    client = TestClient(app)
    response = client.post(
        "/agent/run",
        json={"instruction": "Run shell command: ls"},
    )

    assert response.status_code == 500
    detail = response.json()["detail"]
    assert detail["returncode"] == 2
