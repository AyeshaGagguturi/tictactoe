"""
Pure Tic-Tac-Toe game logic.

Kept deliberately free of any web/framework dependencies so it can be
unit tested in isolation. The API layer wraps this.

Board representation:
    A flat list of 9 strings, indexed 0..8, laid out as:
        0 | 1 | 2
        ---------
        3 | 4 | 5
        ---------
        6 | 7 | 8
    Each cell is "X", "O", or "" (empty).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from uuid import uuid4


class Player(str, Enum):
    X = "X"
    O = "O"


class GameStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    X_WINS = "x_wins"
    O_WINS = "o_wins"
    DRAW = "draw"


# All 8 winning lines: 3 rows, 3 columns, 2 diagonals.
WINNING_LINES: list[tuple[int, int, int]] = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]


class GameError(Exception):
    """Base class for game rule violations. API layer maps these to 400s."""


class GameOverError(GameError):
    """Raised when a move is attempted on a finished game."""


class CellTakenError(GameError):
    """Raised when a move targets an already-occupied cell."""


class InvalidPositionError(GameError):
    """Raised when a position is outside 0..8."""


class WrongTurnError(GameError):
    """Raised when the wrong player tries to move."""


@dataclass
class Game:
    id: str = field(default_factory=lambda: str(uuid4()))
    board: list[str] = field(default_factory=lambda: [""] * 9)
    current_player: Player = Player.X
    status: GameStatus = GameStatus.IN_PROGRESS
    winner: Optional[Player] = None
    winning_line: Optional[tuple[int, int, int]] = None
    move_count: int = 0

    def make_move(self, position: int, player: Player) -> None:
        """Apply a move. Raises GameError subclasses on invalid input."""
        if self.status != GameStatus.IN_PROGRESS:
            raise GameOverError(f"Game is over: {self.status.value}")

        if not isinstance(position, int) or not (0 <= position <= 8):
            raise InvalidPositionError(
                f"Position must be an integer 0..8, got {position!r}"
            )

        if player != self.current_player:
            raise WrongTurnError(
                f"It's {self.current_player.value}'s turn, not {player.value}"
            )

        if self.board[position] != "":
            raise CellTakenError(f"Cell {position} is already taken")

        # Apply move
        self.board[position] = player.value
        self.move_count += 1

        # Check for terminal state
        self._update_status()

        # Swap turn only if game continues
        if self.status == GameStatus.IN_PROGRESS:
            self.current_player = Player.O if player == Player.X else Player.X

    def _update_status(self) -> None:
        """Check the board for a win or draw and update status accordingly."""
        for line in WINNING_LINES:
            a, b, c = line
            if self.board[a] != "" and self.board[a] == self.board[b] == self.board[c]:
                self.winner = Player(self.board[a])
                self.winning_line = line
                self.status = (
                    GameStatus.X_WINS if self.winner == Player.X else GameStatus.O_WINS
                )
                return

        if self.move_count == 9:
            self.status = GameStatus.DRAW

    def reset(self) -> None:
        """Reset to a fresh game, preserving the same id."""
        self.board = [""] * 9
        self.current_player = Player.X
        self.status = GameStatus.IN_PROGRESS
        self.winner = None
        self.winning_line = None
        self.move_count = 0
