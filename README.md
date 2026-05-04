# Tic-Tac-Toe

FastAPI backend + browser UI for Tic-Tac-Toe. In-memory storage, full test coverage.

## Setup

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Run the server

```powershell
uvicorn app.main:app --reload --reload-dir app --port 8000
```

- **Play in browser: `http://localhost:8000`** ← two-player or vs computer
- API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Run the tests

```powershell
pytest -v                          # all tests, verbose
pytest tests\test_game.py -v       # game logic only
pytest tests\test_api.py -v        # API only
pytest -v -k "win"                 # tests matching "win"
pytest --tb=short                  # shorter tracebacks
```

## API

| Method | Path                    | Purpose          |
|--------|-------------------------|------------------|
| GET    | `/`                     | Game UI          |
| GET    | `/health`               | Health check     |
| POST   | `/games`                | Create game      |
| GET    | `/games`                | List all games   |
| GET    | `/games/{id}`           | Get game state   |
| POST   | `/games/{id}/moves`     | Make a move      |
| POST   | `/games/{id}/reset`     | Reset game       |
| DELETE | `/games/{id}`           | Delete game      |

## curl quickstart (PowerShell)

```powershell
# Create a game and capture its id
$response = curl.exe -s -X POST http://localhost:8000/games | ConvertFrom-Json
$GAME_ID = $response.id
Write-Host "Game: $GAME_ID"

# Make a move (X in center)
curl.exe -s -X POST "http://localhost:8000/games/$GAME_ID/moves" `
  -H "Content-Type: application/json" `
  -d '{\"position\": 4, \"player\": \"X\"}' | ConvertFrom-Json | Format-List

# Get current state
curl.exe -s "http://localhost:8000/games/$GAME_ID" | ConvertFrom-Json | Format-List

# Reset
curl.exe -s -X POST "http://localhost:8000/games/$GAME_ID/reset" | ConvertFrom-Json | Format-List
```

## Architecture notes

- **`app/game.py`** — pure game logic. No web framework. Easy to unit test.
- **`app/schemas.py`** — Pydantic request/response models. Validation lives here.
- **`app/main.py`** — thin FastAPI layer that wires HTTP to game logic + serves the UI.
- **`static/index.html`** — single-file browser UI (HTML/CSS/JS). Two-player and vs Computer modes.
- **In-memory store** — `_games` dict in `main.py`. Swap for Redis/Postgres if needed.

## Board layout

```
 0 | 1 | 2
-----------
 3 | 4 | 5
-----------
 6 | 7 | 8
```

## Error model

- **422 Unprocessable Entity** — malformed payload (Pydantic validation, e.g. position out of 0..8, missing field, invalid player value)
- **400 Bad Request** — valid payload but illegal move; body has `{"error": "...", "detail": "..."}` with codes:
  - `cell_taken`
  - `wrong_turn`
  - `game_over`
  - `invalid_position`
- **404 Not Found** — game id doesn't exist

## Talking points for the interview

- **Separation of concerns**: pure logic vs. API layer means logic is testable without spinning up HTTP.
- **Domain errors → HTTP errors**: a single exception handler maps `GameError` subclasses to 400s with stable error codes — easy for clients to handle.
- **Pydantic does cheap validation for free**: position bounds and player enum are enforced at the boundary, so business logic stays clean.
- **Resource-oriented URLs**: `/games/{id}/moves` (POST a move resource) rather than `/move?game=...` — consistent with REST conventions.
- **Same-origin UI**: the frontend is served from FastAPI itself — no CORS, no separate dev server, one `uvicorn` command runs everything.
- **Why no auth / persistence**: scoped to the prompt; would add JWT and Postgres for production. Trade-off worth mentioning, not over-engineering.
