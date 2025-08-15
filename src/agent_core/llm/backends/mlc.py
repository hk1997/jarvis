"""Calls MLC-LLM server."""

from typing import List, Dict, Any

from ..base import BaseLLM


class MLCLLM(BaseLLM):
    """Placeholder for MLC LLM server calls."""

    def chat(self, messages: List[Dict[str, Any]]) -> str:  # type: ignore[override]
        return ""
