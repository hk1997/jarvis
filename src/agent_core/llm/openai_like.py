"""Wrapper for OpenAI-style API."""

from typing import List, Dict, Any

from .base import BaseLLM


class OpenAILike(BaseLLM):
    """Placeholder OpenAI-compatible client."""

    def chat(self, messages: List[Dict[str, Any]]) -> str:  # type: ignore[override]
        """Pretend to send messages to an API."""
        return ""
