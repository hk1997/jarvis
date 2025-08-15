#!/usr/bin/env bash
# Run the FastAPI app for development

uvicorn server.app:app --reload
