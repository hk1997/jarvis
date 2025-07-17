import logging
from typing import List, Dict

import openai
from transformers import pipeline

logger = logging.getLogger(__name__)

class LLMInterface:
    """Abstract interface for language models."""

    def send_prompt(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 500,
        temperature: float = 0.0,
    ) -> str:
        raise NotImplementedError


class OpenAILLM(LLMInterface):
    """LLM implementation using OpenAI's chat completion API."""

    def __init__(self, model: str = "gpt-3.5-turbo") -> None:
        self.model = model

    def send_prompt(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 500,
        temperature: float = 0.0,
    ) -> str:
        response = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        logger.info("OpenAI API call successful")
        return response.choices[0].message.content


class LocalHFLLM(LLMInterface):
    """LLM implementation using a locally hosted Hugging Face model."""

    def __init__(self, model: str = "distilgpt2") -> None:
        self.model = model
        self.generator = pipeline("text-generation", model=model)

    def send_prompt(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 100,
        temperature: float = 0.0,
    ) -> str:
        prompt = "\n".join(m["content"] for m in messages)
        outputs = self.generator(
            prompt, max_new_tokens=max_tokens, temperature=temperature
        )
        return outputs[0]["generated_text"].strip()
