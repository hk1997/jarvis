import json
import logging
from typing import Dict, List

from ..common import LLMInterface, OpenAILLM

logger = logging.getLogger(__name__)


class NewsAggregatorAgent:
    """Agent that generates a daily news digest using a language model."""

    def __init__(self, llm: LLMInterface | None = None) -> None:
        self.llm = llm or OpenAILLM()

    def generate_daily_digest(self) -> Dict[str, List[str]]:
        """Generate and return today's news digest as a structured dict."""
        system_prompt = (
            "You are a helpful news aggregation assistant. "
            "Provide concise bullet summaries for each requested category."
        )
        user_prompt = (
            "Generate today's top news summaries across:\n"
            "- Global Headlines\n"
            "- Finance & Economy\n"
            "- Politics (US, UK, India)\n"
            "- Sports\n"
            "- Science & Tech\n"
            "Respond only with JSON in the specified format."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        logger.info("Requesting news digest from language model")
        response_text = self.llm.send_prompt(messages)

        try:
            digest = json.loads(response_text)
        except json.JSONDecodeError as exc:
            logger.error("Failed to parse JSON response: %s", exc)
            raise ValueError("Invalid JSON from language model") from exc

        return digest

