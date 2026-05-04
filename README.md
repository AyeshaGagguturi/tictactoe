# Tic-Tac-Toe

REST API + browser UI for Tic-Tac-Toe built with **FastAPI**, **Pydantic**, and vanilla JS.  
54 tests · two-player & vs-computer modes · zero external frontend dependencies.

## Quick start

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --reload-dir app --port 8000
```

Open **http://localhost:8000** to play, or explore the API at **http://localhost:8000/docs** (Swagger UI).

## Project structure

```
app/
  game.py       ← pure game logic (no web deps — unit testable in isolation)
  schemas.py    ← Pydantic request/response models (validation at the boundary)
  main.py       ← thin FastAPI layer wiring HTTP → game logic + serves the UI
static/
  index.html    ← single-file browser UI (HTML/CSS/JS, two-player + vs computer)
tests/
  test_game.py  ← game logic unit tests (win detection, draw, invalid moves, reset)
  test_api.py   ← API integration tests (CRUD, error codes, full game flows, frontend)
```

## API

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/` | Browser game UI |
| `GET` | `/health` | Health check |
| `POST` | `/games` | Create a new game → `201` |
| `GET` | `/games` | List all games |
| `GET` | `/games/{id}` | Get game state |
| `POST` | `/games/{id}/moves` | Make a move (`{"position": 0-8, "player": "X"|"O"}`) |
| `POST` | `/games/{id}/undo` | Undo last move |
| `POST` | `/games/{id}/redo` | Redo last undone move |
| `POST` | `/games/{id}/reset` | Reset board (keep same ID) |
| `DELETE` | `/games/{id}` | Delete a game → `204` |

**Errors:** `422` for bad payloads (Pydantic) · `400` for illegal moves (`cell_taken`, `wrong_turn`, `game_over`, `invalid_position`, `no_moves_to_undo`, `no_moves_to_redo`) · `404` for missing games.

## curl quickstart (PowerShell)

```powershell
$response = curl.exe -s -X POST http://localhost:8000/games | ConvertFrom-Json
$GAME_ID = $response.id

# Make a move — X in center
curl.exe -s -X POST "http://localhost:8000/games/$GAME_ID/moves" `
  -H "Content-Type: application/json" `
  -d '{\"position\": 4, \"player\": \"X\"}' | ConvertFrom-Json | Format-List

# Check state
curl.exe -s "http://localhost:8000/games/$GAME_ID" | ConvertFrom-Json | Format-List
```

## Tests

```powershell
pytest -v                          # all 54 tests
pytest tests\test_game.py -v       # game logic only
pytest tests\test_api.py -v        # API + frontend only
```

## Design decisions

| Decision | Rationale |
|----------|-----------|
| **Pure logic layer** (`game.py`) | Testable without HTTP. Swap the API framework and nothing breaks. |
| **Domain errors → HTTP errors** | Single exception handler maps `GameError` subclasses to 400s with stable error codes — clients can branch on `error` field. |
| **Pydantic at the boundary** | Position bounds (0–8) and player enum validated before business logic runs. Keeps `game.py` clean. |
| **Resource-oriented URLs** | `/games/{id}/moves` (POST a move) — not `/move?game=...`. Consistent REST conventions. |
| **Same-origin UI** | Frontend served from FastAPI itself — no CORS config, no separate dev server, one command runs everything. |
| **In-memory store** | Scoped to the exercise. Production would use Postgres + Redis. Deliberate trade-off, not an oversight. |
| **Board as flat list** | Positions 0–8 map to a 3×3 grid. Simpler than 2D array for win detection (`WINNING_LINES` tuples). |
