"""OpenAI Chat schema interface."""

from typing import List, Dict, Any


class BaseLLM:
    """Base LLM interface."""

    def chat(self, messages: List[Dict[str, Any]]) -> str:
        """Placeholder chat method."""
        return ""
