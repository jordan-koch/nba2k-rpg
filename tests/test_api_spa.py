"""ACs 5, 6 and 7 — the two dist states, and the API/SPA boundary between them.

No live server and no socket anywhere in this module.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from fastapi.testclient import TestClient

from rpg_api import create_app

# ─── AC 5 — the missing-build branch (the fresh-clone state) ──────────────────


def test_constructing_against_an_absent_dist_raises_nothing(tmp_path: Path) -> None:
    """The whole reason there is no StaticFiles mount.

    A mount raises RuntimeError right here, so a fresh clone gets a traceback
    on import rather than a running server that explains itself.
    """
    absent = tmp_path / "never-built"

    app = create_app(spa_dist=absent)

    assert app is not None
    assert not absent.exists(), "constructing the app must not create the dist"


def test_api_still_answers_without_a_build(client: TestClient) -> None:
    assert client.get("/api/health").status_code == 200


def test_root_is_503_naming_the_build_command(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 503
    assert "npm run build" in response.text


# ─── AC 6 — the present-build branch ─────────────────────────────────────────


def test_root_serves_index_html_bytes(
    client_factory: Callable[[Path], TestClient], built_spa_dist: Path
) -> None:
    response = client_factory(built_spa_dist).get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    # Bytes, not text: the response is served raw, while read_text would apply
    # universal-newline translation and mask a CRLF mismatch on Windows.
    assert response.content == (built_spa_dist / "index.html").read_bytes()


def test_a_real_asset_is_served(
    client_factory: Callable[[Path], TestClient], built_spa_dist: Path
) -> None:
    response = client_factory(built_spa_dist).get("/assets/index-abc123.js")

    assert response.status_code == 200
    assert "export const ok" in response.text


def test_unknown_path_falls_back_to_the_shell(
    client_factory: Callable[[Path], TestClient], built_spa_dist: Path
) -> None:
    """History fallback: a client-side route is not a 404."""
    response = client_factory(built_spa_dist).get("/careers/some-guy/season/3")

    assert response.status_code == 200
    assert response.content == (built_spa_dist / "index.html").read_bytes()


# ─── AC 7 — the API boundary, asserted on BOTH branches ──────────────────────


def test_unknown_api_path_is_json_404_without_a_build(client: TestClient) -> None:
    response = client.get("/api/does-not-exist")

    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/json")


def test_unknown_api_path_is_json_404_with_a_build(
    client_factory: Callable[[Path], TestClient], built_spa_dist: Path
) -> None:
    """The branch that actually bites.

    With a build present, a naive catch-all hands back index.html with a 200
    for every unknown /api path — so the frontend sees HTML where it expected
    JSON and the bug looks like a frontend parse error.
    """
    response = client_factory(built_spa_dist).get("/api/does-not-exist")

    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/json")
    assert response.content != (built_spa_dist / "index.html").read_bytes()


def test_the_catch_all_did_not_shadow_the_health_route(
    client_factory: Callable[[Path], TestClient], built_spa_dist: Path
) -> None:
    """Registration order, asserted where a build exists to shadow it with."""
    response = client_factory(built_spa_dist).get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ─── Traversal (implementation note, not an acceptance criterion) ─────────────


def test_traversal_outside_the_dist_is_not_served(
    client_factory: Callable[[Path], TestClient], built_spa_dist: Path, tmp_path: Path
) -> None:
    secret = tmp_path / "secret.txt"
    secret.write_text("do not serve me", encoding="utf-8")

    response = client_factory(built_spa_dist).get("/../secret.txt")

    assert "do not serve me" not in response.text
