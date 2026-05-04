"""
FastAPI application exposing the Tic-Tac-Toe game over REST.

Endpoints:
    POST   /games               -> create a new game
    GET    /games               -> list all games (debug aid)
    GET    /games/{id}          -> fetch a game's state
    POST   /games/{id}/moves    -> make a move
    POST   /games/{id}/reset    -> reset a game
    DELETE /games/{id}          -> delete a game

Storage is an in-memory dict; per the prompt, no persistence is needed.
"""

import os

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.game import (
    CellTakenError,
    Game,
    GameError,
    GameOverError,
    InvalidPositionError,
    WrongTurnError,
)
from app.schemas import GameResponse, MoveRequest

app = FastAPI(
    title="Tic-Tac-Toe API",
    description="A simple REST API for playing Tic-Tac-Toe.",
    version="1.0.0",
)

# Serve static assets (CSS, JS, images) from the static/ directory.
_static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=_static_dir), name="static")

# In-memory store: {game_id: Game}.
# Fine for an interview; would swap for Redis/Postgres in production.
_games: dict[str, Game] = {}


def _get_game_or_404(game_id: str) -> Game:
    game = _games.get(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found")
    return game


@app.exception_handler(GameError)
async def game_error_handler(_request, exc: GameError):
    """Map domain errors to 400 with a stable error code."""
    error_code = {
        GameOverError: "game_over",
        CellTakenError: "cell_taken",
        InvalidPositionError: "invalid_position",
        WrongTurnError: "wrong_turn",
    }.get(type(exc), "game_error")
    return JSONResponse(
        status_code=400,
        content={"error": error_code, "detail": str(exc)},
    )


@app.get("/", include_in_schema=False)
def serve_frontend():
    """Serve the game UI at the root URL."""
    return FileResponse(os.path.join(_static_dir, "index.html"))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/games", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
def create_game():
    game = Game()
    _games[game.id] = game
    return GameResponse.from_game(game)


@app.get("/games", response_model=list[GameResponse])
def list_games():
    return [GameResponse.from_game(g) for g in _games.values()]


@app.get("/games/{game_id}", response_model=GameResponse)
def get_game(game_id: str):
    return GameResponse.from_game(_get_game_or_404(game_id))


@app.post("/games/{game_id}/moves", response_model=GameResponse)
def make_move(game_id: str, move: MoveRequest):
    game = _get_game_or_404(game_id)
    game.make_move(move.position, move.player)
    return GameResponse.from_game(game)


@app.post("/games/{game_id}/reset", response_model=GameResponse)
def reset_game(game_id: str):
    game = _get_game_or_404(game_id)
    game.reset()
    return GameResponse.from_game(game)


@app.delete("/games/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game(game_id: str):
    _get_game_or_404(game_id)
    del _games[game_id]
    return None
