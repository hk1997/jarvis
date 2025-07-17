# Jarvis AI Agents

This repository provides a scaffold for a personal collection of AI agents.

## Project Structure

- `frontend/` - Client-side utilities including a simple command line interface.
- `backend/` - FastAPI backend with API routes and session management.
- `ai_engine/` - Core AI logic and agents.
- `main.py` - Entry point to run the FastAPI server.
- `requirements.txt` - Python dependencies.

## Running the Server

Install dependencies and start the server:

```bash
pip install -r requirements.txt
python main.py
```

This will launch a simple FastAPI server with a stub summarization agent.

## Running the CLI

To interact with the agents from your terminal run:

```bash
python -m frontend.cli.cli_launcher
```

On first run you will be asked for your OpenAI API key. If you choose to run a
locally hosted Hugging Face model, the CLI will also prompt for your Hugging
Face API key. These keys are stored in `~/.jarvis_config.json`.
