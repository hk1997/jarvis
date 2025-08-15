"""Optional direct llama.cpp binding."""

from typing import List, Dict, Any

from ..base import BaseLLM


class LlamaCppLLM(BaseLLM):
    """Placeholder for llama.cpp binding."""

    def chat(self, messages: List[Dict[str, Any]]) -> str:  # type: ignore[override]
        return ""
