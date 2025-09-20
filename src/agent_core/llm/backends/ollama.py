"""Client for interacting with a local Ollama server."""

from __future__ import annotations

import os
from typing import Any, Dict, List

import httpx

from ..base import BaseLLM


class OllamaLLM(BaseLLM):
    """Thin wrapper around the Ollama HTTP chat endpoint."""

    def __init__(
        self,
        *,
        host: str | None = None,
        model: str | None = None,
        timeout: float | None = None,
    ) -> None:
        self._host = host or os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
        self._model = model or os.getenv("OLLAMA_MODEL", "gemma3:1b")
        timeout_env = os.getenv("OLLAMA_TIMEOUT", "60")
        try:
            default_timeout = float(timeout_env)
        except (TypeError, ValueError):
            default_timeout = 60.0
        self._timeout = timeout if timeout is not None else default_timeout

    def chat(self, messages: List[Dict[str, Any]]) -> str:  # type: ignore[override]
        payload = {
            "model": self._model,
            "messages": messages,
            "stream": False,
        }

        try:
            response = httpx.post(
                f"{self._host.rstrip('/')}/api/chat",
                json=payload,
                timeout=self._timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:  # pragma: no cover - network failure
            raise RuntimeError(
                f"Failed to reach Ollama server at {self._host}: {exc}"
            ) from exc

        try:
            data: Dict[str, Any] = response.json()
        except ValueError as exc:
            raise RuntimeError("Ollama returned invalid JSON") from exc

        if "error" in data and data["error"]:
            raise RuntimeError(f"Ollama error: {data['error']}")

        message = data.get("message")
        if not isinstance(message, dict):
            raise RuntimeError("Malformed response from Ollama: missing message")

        content = message.get("content", "")
        if not isinstance(content, str):
            raise RuntimeError("Malformed response from Ollama: invalid content")

        return content
