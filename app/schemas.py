"""Pydantic models for API request/response payloads."""

from typing import Optional
from pydantic import BaseModel, Field

from app.game import Game, GameStatus, Player


class MoveRecord(BaseModel):
    position: int
    player: Player


class MoveRequest(BaseModel):
    position: int = Field(..., ge=0, le=8, description="Cell index 0..8")
    player: Player


class GameResponse(BaseModel):
    id: str
    board: list[str]
    current_player: Player
    status: GameStatus
    winner: Optional[Player] = None
    winning_line: Optional[list[int]] = None
    move_count: int
    moves: list[MoveRecord] = []

    @classmethod
    def from_game(cls, game: Game) -> "GameResponse":
        return cls(
            id=game.id,
            board=game.board,
            current_player=game.current_player,
            status=game.status,
            winner=game.winner,
            winning_line=list(game.winning_line) if game.winning_line else None,
            move_count=game.move_count,
            moves=[MoveRecord(position=p, player=pl) for p, pl in game.moves],
        )


class ErrorResponse(BaseModel):
    error: str
    detail: str
