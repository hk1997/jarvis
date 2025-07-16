import logging
import time
from typing import List, Dict

import openai

logger = logging.getLogger(__name__)


def send_prompt(
    messages: List[Dict[str, str]],
    model: str = "gpt-3.5-turbo",
    max_tokens: int = 500,
    temperature: float = 0.0,
    max_retries: int = 3,
) -> str:
    """Send a chat completion request to OpenAI with retries."""
    for attempt in range(max_retries):
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            logger.info("OpenAI API call successful")
            return response.choices[0].message.content
        except Exception as exc:  # broad except for simplicity
            logger.error("OpenAI API error: %s", exc)
            if attempt >= max_retries - 1:
                raise
            time.sleep(2 ** attempt)

