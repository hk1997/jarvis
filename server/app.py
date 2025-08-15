"""FastAPI app exposing /chat, /tools, /health."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}
