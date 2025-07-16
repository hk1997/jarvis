import logging

logger = logging.getLogger(__name__)

# Placeholder summarization agent

def summarize(text: str) -> str:
    logger.info("Summarizing text")
    # Simple stub that returns the first 20 words
    return " ".join(text.split()[:20])

