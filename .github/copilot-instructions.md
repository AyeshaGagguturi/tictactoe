# Copilot Instructions

## Project context

This is a FastAPI Tic-Tac-Toe app with a browser UI (`static/index.html`) served from the same server. The API runs on `uvicorn` (default port 8000). Environment is Windows/PowerShell.

## Verification requirements

After any medium-or-larger code change (new routes, static serving changes, config changes, dependency updates, or anything that affects runtime behavior):

1. **Run unit tests first:** `pytest --tb=short -q`
2. **Start the server live** on a free port and verify affected endpoints with real HTTP requests (use `curl.exe` or `Invoke-WebRequest`). Do not treat passing unit tests alone as sufficient for integration-level changes.
3. **Smoke-test the UI route** (`GET /`) whenever changes touch static file serving, route ordering, or middleware — confirm `200` with `text/html` content type.
4. **Only commit after live verification passes.**

## Common pitfalls

- **FastAPI mount ordering:** `app.mount()` for static files must come AFTER all route definitions, otherwise mounts shadow path-based routes (e.g., `GET /` returns 404).
- **Uvicorn reload:** Always use `--reload-dir app` to avoid watching `venv/` which causes crash loops.
- **Port conflicts:** If port 8000 is in use, pick another port (8001, 8002, etc.) for testing.

## Tech stack

- Python 3.12, FastAPI, Uvicorn, Pydantic
- Tests: pytest + httpx (TestClient)
- No database — in-memory dict store
- Single-file frontend: `static/index.html`
