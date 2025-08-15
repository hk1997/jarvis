"""Calls local Ollama server."""

from typing import List, Dict, Any

from ..base import BaseLLM


class OllamaLLM(BaseLLM):
    """Placeholder for Ollama server calls."""

    def chat(self, messages: List[Dict[str, Any]]) -> str:  # type: ignore[override]
        return ""
