"""Small convenience script to ping a local Ollama server."""

from __future__ import annotations

import argparse
import sys
from typing import List, Dict, Any

from agent_core.llm.backends.ollama import OllamaLLM


def build_messages(prompt: str) -> List[Dict[str, Any]]:
    """Generate a minimal chat payload for the given prompt."""

    return [
        {"role": "system", "content": "You are a concise assistant."},
        {"role": "user", "content": prompt},
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "prompt",
        nargs="?",
        default="Say hello in one sentence.",
        help="User prompt to send to the Ollama chat endpoint.",
    )
    parser.add_argument(
        "--model",
        help="Override the Ollama model name (defaults to env/constructor default).",
    )
    parser.add_argument(
        "--host",
        help="Override the Ollama host URL (defaults to env/constructor default).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        help="Override the request timeout in seconds (defaults to env/constructor default).",
    )

    args = parser.parse_args(argv)

    llm = OllamaLLM(host=args.host, model=args.model, timeout=args.timeout)
    messages = build_messages(args.prompt)

    response = llm.chat(messages)
    print(response)

    return 0


if __name__ == "__main__":  # pragma: no cover - script entry point
    sys.exit(main())
