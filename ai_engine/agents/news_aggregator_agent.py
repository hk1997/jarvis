import json
import logging
from typing import Dict, List

from ..common.gpt_utils import send_prompt

logger = logging.getLogger(__name__)


class NewsAggregatorAgent:
    """Agent that generates a daily news digest using ChatGPT."""

    def __init__(self, model: str = "gpt-3.5-turbo") -> None:
        self.model = model

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

        logger.info("Requesting news digest from OpenAI")
        response_text = send_prompt(messages, model=self.model)

        try:
            digest = json.loads(response_text)
        except json.JSONDecodeError as exc:
            logger.error("Failed to parse JSON response: %s", exc)
            raise ValueError("Invalid JSON from OpenAI") from exc

        return digest

