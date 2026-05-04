"""API integration tests using FastAPI's TestClient."""

import pytest
from fastapi.testclient import TestClient

from app.main import _games, app


@pytest.fixture(autouse=True)
def clear_games():
    """Reset in-memory store before each test for isolation."""
    _games.clear()
    yield
    _games.clear()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def game_id(client):
    """Create a fresh game and return its id."""
    response = client.post("/games")
    return response.json()["id"]


class TestFrontend:
    def test_root_serves_html(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_root_contains_game_title(self, client):
        response = client.get("/")
        assert "Tic-Tac-Toe" in response.text

    def test_static_index_accessible(self, client):
        response = client.get("/static/index.html")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestHealth:
    def test_health_returns_ok(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestCreateGame:
    def test_create_returns_201(self, client):
        response = client.post("/games")
        assert response.status_code == 201

    def test_created_game_is_empty(self, client):
        response = client.post("/games")
        body = response.json()
        assert body["board"] == [""] * 9
        assert body["current_player"] == "X"
        assert body["status"] == "in_progress"
        assert body["move_count"] == 0
        assert body["winner"] is None

    def test_create_game_has_id(self, client):
        body = client.post("/games").json()
        assert "id" in body and isinstance(body["id"], str) and body["id"]


class TestGetGame:
    def test_get_existing_game(self, client, game_id):
        response = client.get(f"/games/{game_id}")
        assert response.status_code == 200
        assert response.json()["id"] == game_id

    def test_get_missing_game_returns_404(self, client):
        response = client.get("/games/does-not-exist")
        assert response.status_code == 404


class TestListGames:
    def test_empty_list(self, client):
        assert client.get("/games").json() == []

    def test_list_after_creating(self, client):
        client.post("/games")
        client.post("/games")
        assert len(client.get("/games").json()) == 2


class TestMakeMove:
    def test_valid_move_updates_board(self, client, game_id):
        response = client.post(
            f"/games/{game_id}/moves", json={"position": 4, "player": "X"}
        )
        assert response.status_code == 200
        body = response.json()
        assert body["board"][4] == "X"
        assert body["current_player"] == "O"
        assert body["move_count"] == 1

    def test_move_on_taken_cell_returns_400(self, client, game_id):
        client.post(f"/games/{game_id}/moves", json={"position": 0, "player": "X"})
        response = client.post(
            f"/games/{game_id}/moves", json={"position": 0, "player": "O"}
        )
        assert response.status_code == 400
        assert response.json()["error"] == "cell_taken"

    def test_move_with_wrong_player_returns_400(self, client, game_id):
        response = client.post(
            f"/games/{game_id}/moves", json={"position": 0, "player": "O"}
        )
        assert response.status_code == 400
        assert response.json()["error"] == "wrong_turn"

    @pytest.mark.parametrize("bad_pos", [-1, 9, 100])
    def test_out_of_range_position_returns_422(self, client, game_id, bad_pos):
        # Pydantic catches this at the validation layer (422), not 400
        response = client.post(
            f"/games/{game_id}/moves", json={"position": bad_pos, "player": "X"}
        )
        assert response.status_code == 422

    def test_invalid_player_value_returns_422(self, client, game_id):
        response = client.post(
            f"/games/{game_id}/moves", json={"position": 0, "player": "Z"}
        )
        assert response.status_code == 422

    def test_missing_field_returns_422(self, client, game_id):
        response = client.post(f"/games/{game_id}/moves", json={"position": 0})
        assert response.status_code == 422

    def test_move_on_missing_game_returns_404(self, client):
        response = client.post(
            "/games/missing/moves", json={"position": 0, "player": "X"}
        )
        assert response.status_code == 404


class TestFullGameFlow:
    def test_x_wins_top_row(self, client, game_id):
        moves = [(0, "X"), (3, "O"), (1, "X"), (4, "O"), (2, "X")]
        for pos, player in moves:
            response = client.post(
                f"/games/{game_id}/moves", json={"position": pos, "player": player}
            )
            assert response.status_code == 200

        final = response.json()
        assert final["status"] == "x_wins"
        assert final["winner"] == "X"
        assert sorted(final["winning_line"]) == [0, 1, 2]

    def test_cannot_move_after_game_ends(self, client, game_id):
        moves = [(0, "X"), (3, "O"), (1, "X"), (4, "O"), (2, "X")]
        for pos, player in moves:
            client.post(
                f"/games/{game_id}/moves", json={"position": pos, "player": player}
            )
        response = client.post(
            f"/games/{game_id}/moves", json={"position": 8, "player": "O"}
        )
        assert response.status_code == 400
        assert response.json()["error"] == "game_over"

    def test_draw_scenario(self, client, game_id):
        moves = [(0, "X"), (1, "O"), (2, "X"), (4, "O"),
                 (3, "X"), (5, "O"), (7, "X"), (6, "O"), (8, "X")]
        for pos, player in moves:
            response = client.post(
                f"/games/{game_id}/moves", json={"position": pos, "player": player}
            )
        final = response.json()
        assert final["status"] == "draw"
        assert final["winner"] is None
        assert final["move_count"] == 9


class TestResetAndDelete:
    def test_reset_clears_board(self, client, game_id):
        client.post(f"/games/{game_id}/moves", json={"position": 0, "player": "X"})
        response = client.post(f"/games/{game_id}/reset")
        assert response.status_code == 200
        body = response.json()
        assert body["board"] == [""] * 9
        assert body["move_count"] == 0
        assert body["id"] == game_id

    def test_delete_removes_game(self, client, game_id):
        assert client.delete(f"/games/{game_id}").status_code == 204
        assert client.get(f"/games/{game_id}").status_code == 404

    def test_delete_missing_game_returns_404(self, client):
        assert client.delete("/games/missing").status_code == 404
