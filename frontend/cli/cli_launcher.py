import json
import os
import logging
from getpass import getpass

import openai

from ai_engine.agents.news_aggregator_agent import NewsAggregatorAgent
from ai_engine.agents.summarizer import summarize
from ai_engine.common import OpenAILLM, LocalHFLLM, LLMInterface

CONFIG_PATH = os.path.expanduser("~/.jarvis_config.json")
logger = logging.getLogger(__name__)


def load_or_create_config():
    """Load configuration or create it by prompting the user for missing keys."""
    config: dict = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as exc:  # corrupt file etc
            logger.error("Failed to read config: %s", exc)

    if not config.get("openai_api_key"):
        print("OpenAI API key not found. Please enter it now.")
        config["openai_api_key"] = getpass("OpenAI API Key: ").strip()

    return config


def save_config(config: dict) -> None:
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f)
        print(f"Configuration saved to {CONFIG_PATH}")
    except Exception as exc:
        logger.error("Failed to write config file: %s", exc)


def choose_agent() -> str:
    """Prompt the user to select an agent."""
    print("Select an agent to run:")
    print("1. News Aggregator")
    print("2. Summarizer")
    return input("Enter choice number: ").strip()


def choose_llm() -> str:
    """Prompt the user to select which language model to use."""
    print("Select language model:")
    print("1. OpenAI (cloud)")
    print("2. Local Hugging Face model")
    return input("Enter choice number: ").strip()


def main():
    logging.basicConfig(level=logging.INFO)
    config = load_or_create_config()

    llm_choice = choose_llm()
    llm: LLMInterface
    if llm_choice == "1":
        openai.api_key = config.get("openai_api_key")
        llm = OpenAILLM()
    elif llm_choice == "2":
        if not config.get("hf_api_key"):
            print("HuggingFace API key not found. Please enter it now.")
            config["hf_api_key"] = getpass("HuggingFace API Key: ").strip()
            save_config(config)
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = config["hf_api_key"]
        llm = LocalHFLLM()
    else:
        print("Invalid model choice")
        return

    choice = choose_agent()
    if choice == "1":
        agent = NewsAggregatorAgent(llm=llm)
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
