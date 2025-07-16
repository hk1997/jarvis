import logging
from fastapi import FastAPI
from .routes import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Jarvis AI Backend")
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    logger.info("Backend starting up")

