# ai-agent

Local-first, multi-agent AI project scaffold.

## Prerequisites

- Python 3.11 (match the version declared in `pyproject.toml`)
- [Poetry](https://python-poetry.org/)
- [Ollama](https://ollama.ai/) if you want local LLM responses

## Project setup with Poetry

1. Clone the repository and enter the project directory:
   ```bash
   git clone <repo-url>
   cd jarvis
   ```
2. Point Poetry at your Python 3.11 interpreter (adjust the path to match your system):
   ```bash
   poetry env use /usr/local/bin/python3.11
   ```
3. Install dependencies (add dev tooling if needed):
   ```bash
   poetry install --extras dev
   ```
   Omit `--extras dev` if you do not want the optional linting and test tools.

## Running the FastAPI app

Start the development server inside the Poetry environment:
```bash
poetry run ./scripts/dev_run.sh
```
The server runs at `http://127.0.0.1:8000` and exposes `/chat`, `/tools`, and `/health` endpoints.

## Using a local Ollama model

1. Install and launch Ollama, then start your preferred model. The defaults expect `gemma3:1b`:
   ```bash
   ollama run gemma3:1b
   ```
2. (Optional) Configure environment variables to point at a different host or model:
   ```bash
   export OLLAMA_HOST='http://127.0.0.1:11434'
   export OLLAMA_MODEL='gemma3:1b'
   export OLLAMA_TIMEOUT='60'
   ```
3. Smoke test the integration using the helper script:
   ```bash
   poetry run python scripts/ollama_smoke_test.py "Say hello in one sentence."
   ```

## Running tests

```bash
poetry run pytest
```
