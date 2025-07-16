import json
import os
import logging
from getpass import getpass

import openai

from ai_engine.agents.news_aggregator_agent import NewsAggregatorAgent
from ai_engine.agents.summarizer import summarize

CONFIG_PATH = os.path.expanduser("~/.jarvis_config.json")
logger = logging.getLogger(__name__)


def load_or_create_config():
    """Load configuration or create it by prompting the user."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
                if "openai_api_key" in config and config["openai_api_key"]:
                    return config
        except Exception as exc:  # corrupt file etc
            logger.error("Failed to read config: %s", exc)

    print("OpenAI API key not found. Please enter it now.")
    api_key = getpass("OpenAI API Key: ").strip()
    config = {"openai_api_key": api_key}
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f)
        print(f"Configuration saved to {CONFIG_PATH}")
    except Exception as exc:
        logger.error("Failed to write config file: %s", exc)
    return config


def choose_agent() -> str:
    """Prompt the user to select an agent."""
    print("Select an agent to run:")
    print("1. News Aggregator")
    print("2. Summarizer")
    return input("Enter choice number: ").strip()


def main():
    logging.basicConfig(level=logging.INFO)
    config = load_or_create_config()
    openai.api_key = config.get("openai_api_key")

    choice = choose_agent()
    if choice == "1":
        agent = NewsAggregatorAgent()
        digest = agent.generate_daily_digest()
        print(json.dumps(digest, indent=2))
    elif choice == "2":
        text = input("Enter text to summarize: ")
        summary = summarize(text)
        print("Summary:\n" + summary)
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
