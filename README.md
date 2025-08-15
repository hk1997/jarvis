# ai-agent

Local-first, multi-agent AI project scaffold.

## Running locally

1. Install [Poetry](https://python-poetry.org/) and install dependencies:
   ```bash
   poetry install
   ```
2. Run the development server:
   ```bash
   ./scripts/dev_run.sh
   ```

The FastAPI app exposes `/chat`, `/tools`, and `/health` endpoints.
