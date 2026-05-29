# Repository Guidelines

## Project Structure & Module Organization

This repository contains a small FastAPI banking support agent. The API entry point is `app/main.py`, with `run.py` starting Uvicorn locally. Workflow orchestration lives in `app/agent/orchestrator.py`, which calls node implementations in `app/nodes/` for intent detection, priority assessment, policy retrieval, drafting, validation, and routing. Shared Pydantic models and settings are in `app/core/`; external model clients are in `app/clients/`; static banking policy snippets are in `app/data/policies.py`. Example request payloads are stored in `examples/sample_requests.json`. Keep generated caches such as `__pycache__/` out of commits.

## Build, Test, and Development Commands

- `python -m venv .venv && source .venv/bin/activate`: create and activate a local virtual environment.
- `pip install -r requirements.txt`: install FastAPI, Pydantic, model, and client dependencies.
- `python run.py`: run the API at `http://localhost:8000` with reload enabled.
- `python -c "import json, requests; [print(requests.post('http://localhost:8000/support', json=t).json()) for t in json.load(open('examples/sample_requests.json'))]"`: smoke-test the `/support` endpoint against sample inputs after the server starts.

## Coding Style & Naming Conventions

Use Python 3.10+ and follow standard PEP 8 conventions: 4-space indentation, `snake_case` for functions and variables, `PascalCase` for Pydantic models and node classes. Keep each workflow step isolated in its node module and expose a simple `execute(...)` method when adding new nodes. Prefer explicit typed schemas in `app/core/schemas.py` for request, response, and trace data instead of unstructured dictionaries.

## Testing Guidelines

No automated test suite is currently checked in. For changes, add focused tests under a new `tests/` directory using `pytest`, with names like `test_router_node.py` or `test_support_endpoint.py`. Mock external LLM and intent API calls; do not require Pinggy, Ollama, or Kaggle endpoints for unit tests. Until tests exist, run the sample-request smoke test and inspect the response `decision`, `final_reply`, and `trace`.

## Commit & Pull Request Guidelines

The current history uses short imperative messages such as `complete project` and `update video link to README`. Keep commits concise and task-focused. Pull requests should describe the behavior changed, list manual or automated tests run, mention any configuration changes, and include screenshots or response samples when API output changes.

## Security & Configuration Tips

Runtime settings are loaded from environment variables or `.env` via `app/core/settings.py`. Do not commit real tunnel URLs, credentials, API keys, or generated result files. Document any required local services, especially the Ollama model name and intent prediction endpoint.
