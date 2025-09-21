"""FastAPI app exposing /chat, /tools, /health."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent_core.graph import AgentGraph
from agent_core.tools.shell import ShellCommandError


class InstructionRequest(BaseModel):
    """Payload for agent instructions."""

    instruction: str


class InstructionResponse(BaseModel):
    """Agent execution result."""

    output: str


app = FastAPI()
app.state.agent = AgentGraph()


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/agent/run", response_model=InstructionResponse)
async def run_instruction(payload: InstructionRequest) -> InstructionResponse:
    """Execute an instruction via the AgentGraph."""

    agent: AgentGraph = app.state.agent

    try:
        output = agent.handle_instruction(payload.instruction)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except ShellCommandError as exc:
        raise HTTPException(
            status_code=500,
            detail={
                "message": str(exc),
                "returncode": exc.returncode,
                "output": exc.output,
            },
        ) from exc

    return InstructionResponse(output=output)
