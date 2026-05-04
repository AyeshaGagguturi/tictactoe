"""Unit tests for the pure game logic. No FastAPI involved."""

import pytest

from app.game import (
    CellTakenError,
    Game,
    GameOverError,
    GameStatus,
    InvalidPositionError,
    Player,
    WrongTurnError,
)


class TestGameInitialization:
    def test_new_game_has_empty_board(self):
        game = Game()
        assert game.board == [""] * 9
        assert game.move_count == 0

    def test_x_starts(self):
        assert Game().current_player == Player.X

    def test_new_game_in_progress(self):
        game = Game()
        assert game.status == GameStatus.IN_PROGRESS
        assert game.winner is None
        assert game.winning_line is None

    def test_each_game_has_unique_id(self):
        assert Game().id != Game().id


class TestValidMoves:
    def test_first_move_places_x(self):
        game = Game()
        game.make_move(4, Player.X)
        assert game.board[4] == "X"
        assert game.move_count == 1

    def test_turn_alternates_after_move(self):
        game = Game()
        game.make_move(0, Player.X)
        assert game.current_player == Player.O
        game.make_move(1, Player.O)
        assert game.current_player == Player.X

    def test_move_count_increments(self):
        game = Game()
        for i, p in enumerate([Player.X, Player.O, Player.X]):
            game.make_move(i, p)
        assert game.move_count == 3


class TestInvalidMoves:
    def test_cell_taken_raises(self):
        game = Game()
        game.make_move(0, Player.X)
        with pytest.raises(CellTakenError):
            game.make_move(0, Player.O)

    @pytest.mark.parametrize("pos", [-1, 9, 100, -100])
    def test_out_of_range_position_raises(self, pos):
        game = Game()
        with pytest.raises(InvalidPositionError):
            game.make_move(pos, Player.X)

    def test_wrong_player_turn_raises(self):
        game = Game()
        with pytest.raises(WrongTurnError):
            game.make_move(0, Player.O)

    def test_wrong_player_turn_after_first_move(self):
        game = Game()
        game.make_move(0, Player.X)
        with pytest.raises(WrongTurnError):
            game.make_move(1, Player.X)


class TestWinDetection:
    @pytest.mark.parametrize(
        "winning_moves",
        [
            [0, 1, 2],  # top row
            [3, 4, 5],  # middle row
            [6, 7, 8],  # bottom row
            [0, 3, 6],  # left column
            [1, 4, 7],  # middle column
            [2, 5, 8],  # right column
            [0, 4, 8],  # diagonal
            [2, 4, 6],  # anti-diagonal
        ],
    )
    def test_x_can_win_on_each_line(self, winning_moves):
        """X wins by playing the 3 winning cells while O plays elsewhere."""
        game = Game()
        # Pick 3 distinct O moves that don't overlap with X's winning line
        o_moves = [i for i in range(9) if i not in winning_moves][:3]

        # Interleave: X, O, X, O, X
        game.make_move(winning_moves[0], Player.X)
        game.make_move(o_moves[0], Player.O)
        game.make_move(winning_moves[1], Player.X)
        game.make_move(o_moves[1], Player.O)
        game.make_move(winning_moves[2], Player.X)

        assert game.status == GameStatus.X_WINS
        assert game.winner == Player.X
        assert set(game.winning_line) == set(winning_moves)

    def test_o_can_win(self):
        game = Game()
        # X: 0, 1, 5  |  O: 4, 2, 6  -> O wins anti-diagonal (2, 4, 6)
        for pos, player in [(0, Player.X), (4, Player.O),
                            (1, Player.X), (2, Player.O),
                            (5, Player.X), (6, Player.O)]:
            game.make_move(pos, player)
        assert game.status == GameStatus.O_WINS
        assert game.winner == Player.O

    def test_no_move_after_win(self):
        game = Game()
        # X wins top row
        for pos, player in [(0, Player.X), (3, Player.O),
                            (1, Player.X), (4, Player.O),
                            (2, Player.X)]:
            game.make_move(pos, player)
        with pytest.raises(GameOverError):
            game.make_move(8, Player.O)

    def test_current_player_does_not_swap_after_winning_move(self):
        """Subtle: after X's winning move, current_player stays X (the winner)."""
        game = Game()
        for pos, player in [(0, Player.X), (3, Player.O),
                            (1, Player.X), (4, Player.O),
                            (2, Player.X)]:
            game.make_move(pos, player)
        assert game.current_player == Player.X


class TestDraw:
    def test_full_board_with_no_winner_is_draw(self):
        game = Game()
        # Classic draw sequence:
        # X | O | X
        # X | O | O
        # O | X | X
        moves = [(0, Player.X), (1, Player.O),
                 (2, Player.X), (4, Player.O),
                 (3, Player.X), (5, Player.O),
                 (7, Player.X), (6, Player.O),
                 (8, Player.X)]
        for pos, player in moves:
            game.make_move(pos, player)
        assert game.status == GameStatus.DRAW
        assert game.winner is None
        assert game.move_count == 9

    def test_no_move_after_draw(self):
        game = Game()
        moves = [(0, Player.X), (1, Player.O),
                 (2, Player.X), (4, Player.O),
                 (3, Player.X), (5, Player.O),
                 (7, Player.X), (6, Player.O),
                 (8, Player.X)]
        for pos, player in moves:
            game.make_move(pos, player)
        with pytest.raises(GameOverError):
            game.make_move(0, Player.O)


class TestReset:
    def test_reset_clears_board_and_state(self):
        game = Game()
        original_id = game.id
        game.make_move(0, Player.X)
        game.make_move(1, Player.O)
        game.reset()
        assert game.id == original_id  # id preserved
        assert game.board == [""] * 9
        assert game.current_player == Player.X
        assert game.status == GameStatus.IN_PROGRESS
        assert game.move_count == 0
