from fastapi import APIRouter
from ai_engine.agents import summarizer
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/status")
async def status():
    logger.info("Status endpoint called")
    return {"status": "ok"}

@router.post("/summarize")
async def summarize(text: str):
    logger.info("Summarize endpoint called")
    return {"summary": summarizer.summarize(text)}

